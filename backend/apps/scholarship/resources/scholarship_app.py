from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from apps.scholarship.models import ScholarshipApplication, Student
from apps.api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'department']
        
        
        
class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)    

    class Meta:
        model = ScholarshipApplication
        fields = [
            "student", "scholarship", "status"
        ]
        read_only_fields = ["id"]


class ScholarshipApplicationViewset(ModelViewSet):
    queryset = ScholarshipApplication.objects.all()
    serializer_class = ScholarshipApplicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
