from django.conf import settings
import random
import string
# Rest Framework Serializers
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import Subject,Enroll
from accounts.serializers import CustomUserSerializer

class SubjectSerializer(serializers.ModelSerializer):
    subjectName = serializers.CharField(max_length=255)
    subjectTimeList = serializers.CharField()
    subjectInstructorId = CustomUserSerializer(read_only=True)
    subjectClass = serializers.IntegerField()
    subjectGrade = serializers.IntegerField()
    invitationCode = serializers.CharField(max_length=16, required=False , allow_null = True)
    class Meta:
        model = Subject
        fields = '__all__'

class EnrollSerializer(serializers.ModelSerializer):
    userId = CustomUserSerializer(read_only=True)
    subjectId = SubjectSerializer(read_only=True)
    class Meta:
        model = Enroll
        fields = '__all__'


class EnrollSubjectSerializer(serializers.ModelSerializer):
    invitationCode = serializers.CharField(max_length=16)
    class Meta:
        model = Subject
        fields = ('invitationCode',)

class SubjectSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'




