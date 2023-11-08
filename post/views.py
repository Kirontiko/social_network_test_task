from datetime import datetime

from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from post.models import Post
from post.serializers import (
    PostListSerializer,
    PostSerializer,
    LikesAnalyticsSerializer,
)


class PostViewSet(ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.annotate(total_likes=Count("likes")).order_by("-created_at")
    permission_classes = [
        IsAuthenticated,
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["GET"],
        detail=True,
        url_path="like",
    )
    def like(self, request, pk=None) -> Response:
        post = self.get_object()
        user = request.user

        if post.likes.filter(id=user.id).exists():
            response_data = {"message": "You`ve already liked this post before"}

            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)

        post.likes.add(user)

        response_data = {
            "message": f"You`ve successfully liked post from {post.author}"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        url_path="unlike",
    )
    def unlike(self, request, pk=None) -> Response:
        post = self.get_object()
        user = request.user
        user.last_request = timezone.now()
        user.save()

        if not post.likes.filter(id=user.id).exists():
            response_data = {"message": "You haven`t liked this post"}

            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)

        post.likes.remove(user)

        response_data = {
            "message": f"You`ve successfully removed like from {post.author} post"
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AnalyticsViewSet(ModelViewSet):
    serializer_class = LikesAnalyticsSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        date_to = datetime.strptime(date_to, "%Y-%m-%d").date()

        return (
            Post.objects.filter(created_at__range=[date_from, date_to])
            .values("created_at__date")
            .annotate(total_likes=Count("likes"))
        )
