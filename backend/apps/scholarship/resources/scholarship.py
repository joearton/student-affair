from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from apps.scholarship.models import Scholarship
from apps.api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)


class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = ["id", "name", "attachments"]
        read_only_fields = ["id"]
  

class ScholarshipViewset(ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
