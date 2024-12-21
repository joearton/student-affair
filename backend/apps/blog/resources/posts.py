from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from apps.blog.models import Category, Post, Tag
from apps.api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email'] 



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]
        

class PostSerializer(serializers.ModelSerializer):
    publication_date = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
        
    class Meta:
        model = Post
        fields = [
            "id", "title", "subtitle", "slug",
            "author", "content", "publication_date",
            "kind", "status", "featured_image",
            "categories", "tags"
        ]
        read_only_fields = ["id", "publication_date"]

    def validate_slug(self, value):
        """Ensure the slug is unique."""
        if Post.objects.filter(slug=value).exists():
            raise serializers.ValidationError("A post with this slug already exists.")
        return value

    def get_publication_date(self, obj):
        return obj.publication_date
  

class PostViewset(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug' 
    search_fields = ['title', 'content', 'categories__name', 'tags__name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_keyword = self.request.query_params.get('search', None)
        category_name = self.request.query_params.get('category', None)
        tag_name = self.request.query_params.get('tag', None)
        slug = self.request.query_params.get('slug', None)
        post_id = self.request.query_params.get('id', None)
        
        if search_keyword:
            queryset  = queryset.filter(title__icontains=search_keyword)
            queryset |= queryset.filter(content__icontains=search_keyword)
            
        if category_name:
            queryset = queryset.filter(categories__name__iexact=category_name)

        if tag_name:
            queryset = queryset.filter(tags__name__iexact=tag_name)

        if slug:
            queryset = queryset.filter(slug=slug)

        if post_id:
            queryset = queryset.filter(id=post_id)
            
        return queryset.distinct()