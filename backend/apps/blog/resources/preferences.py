from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import serializers
from apps.blog.models import Preference, Slideshow, Navbar, SocialMedia
from rest_framework.response import Response


class SlideshowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slideshow
        fields = ['id', 'title', 'image', 'link', 'order', 'preference']
                

class NavbarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navbar
        fields = ['id', 'title', 'link', 'icon', 'order', 'preference']


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url', 'preference']



class PreferenceSerializer(serializers.ModelSerializer):
    slideshows = SlideshowSerializer(many=True, read_only=True)
    navbars = NavbarSerializer(many=True, read_only=True)    
    social_medias = SocialMediaSerializer(read_only=True)
    
    class Meta:
        model = Preference
        fields = [
            'id', 
            'site_title', 
            'site_subtitle', 
            'site_description', 
            'site_logo', 
            'site_favicon', 
            'contact_email', 
            'contact_phone', 
            'slideshows', 
            'navbars',
            'social_medias'
        ]
        read_only_fields = ['id']


        
class PreferenceViewSet(ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        first_object = self.get_queryset().first()
        if first_object:
            serializer = self.get_serializer(first_object)
            return Response(serializer.data)
        return Response({"detail": "No data found"}, status=404)