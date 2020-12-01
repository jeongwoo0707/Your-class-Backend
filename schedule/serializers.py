from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import Assignment, Submit
from accounts.serializers import CustomUserSerializer
from subject.serializers import SubjectSerializer,SubjectSimpleSerializer

class ScheduleSerializer(serializers.ModelSerializer):
    userId = CustomUserSerializer(required=False, read_only=True)