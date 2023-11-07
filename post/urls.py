from django.urls import path

from post.views import PostViewSet

app_name = "post"

urlpatterns = [
    path("posts/", PostViewSet.as_view({"get": "list"}), name="posts"),
    path('posts/<int:pk>/like/', PostViewSet.as_view({"get": "like"}), name='post-like'),
    path("posts/<int:pk>/unlike/", PostViewSet.as_view({"get": "unlike"}))
]