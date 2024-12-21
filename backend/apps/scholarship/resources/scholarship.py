from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from apps.scholarship.models import Scholarship, Faculty, Unit
from apps.api.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny, IsAdminUser, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["name"]

class FacultySerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    class Meta:
        model = Faculty
        fields = ["unit"]

class ScholarshipSerializer(serializers.ModelSerializer):
    unit_names = serializers.SerializerMethodField()
    class Meta:
        model = Scholarship
        fields = [
            "id", "name", "description", "requirement", "attachments", "status", 
            "source", "destination", "start_date", "end_date", "quota", 
            "faculties", "departments", "targets", "thumbnail"
        ]
        read_only_fields = ["id"]

    def get_unit_names(self, obj):
        return [faculty.unit.name for faculty in obj.faculties.all() if faculty.unit]

class ScholarshipViewset(ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
