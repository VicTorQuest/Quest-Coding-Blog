from rest_framework import serializers
from .models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'url', 'created_at',]

    def get_url(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Post):
            return None
        return obj.get_post_url

class CreatePostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'intro',
            'post_img',
            'content',
        ]

        extra_kwargs = {
            'category': { 'read_only': True }
        }
