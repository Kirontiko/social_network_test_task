from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from post.models import Post
from post.serializers import PostListSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.annotate(total_likes=Count("likes")).order_by("-created_at")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        if self.request.method == "POST":
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
            response_data = {
                "message": "You`ve already liked this post before"
            }

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

        if not post.likes.filter(id=user.id).exists():
            response_data = {
                "message": "You haven`t liked this post"
            }

            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)

        post.likes.remove(user)

        response_data = {
            "message": f"You`ve successfully removed like from {post.author} post"
        }

        return Response(response_data, status=status.HTTP_200_OK)


