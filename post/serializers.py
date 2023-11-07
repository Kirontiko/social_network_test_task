from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "content", "author")
        read_only_fields = ("id", "author")


class PostListSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(read_only=True)
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = ("id", "content", "author_name", "created_at", "total_likes")
