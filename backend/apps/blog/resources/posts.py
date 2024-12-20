from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from apps.blog.models import Post
from apps.api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)


class PostSerializer(serializers.ModelSerializer):
    publication_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ["id", "title", "subtitle", "slug", "author", "content", "publication_date", "kind", "status", "featured_image",]
        read_only_fields = ["id", "publication_date"]

    def validate_slug(self, value):
        """Ensure the slug is unique."""
        if Post.objects.filter(slug=value).exists():
            raise serializers.ValidationError("A post with this slug already exists.")
        return value

    def get_publication_date(self, obj):
        return obj.publication_date.strftime('%d-%m-%Y')
  

class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug' 
    
