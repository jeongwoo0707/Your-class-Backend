from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import Assignment, Submit
from accounts.serializers import CustomUserSerializer
from subject.serializers import SubjectSerializer,SubjectSimpleSerializer

class AssignmentSerializer(serializers.ModelSerializer):
    subjectId = SubjectSimpleSerializer(required=False, read_only=True, allow_null = True)
    assignmentName = serializers.CharField(max_length=255)
    assignmentDetail = serializers.CharField(allow_null=True, allow_blank=True)
    assignmentFile = serializers.FileField(required=False, allow_null=True)
    assignmentFileName = serializers.CharField(required=False, max_length=64, allow_null=True, allow_blank=True)
    assignmentUpdateDate = serializers.DateTimeField(required=False)
    assignmentDueDate = serializers.DateTimeField()
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmitSerializer(serializers.ModelSerializer):
    assignmentId = AssignmentSerializer(required=False, read_only = True)
    submitUpdateDate = serializers.DateTimeField(required=False)
    submitDetail = serializers.CharField(allow_null=True, allow_blank=True)
    submitFile = serializers.FileField(required=False, allow_null=True)
    submitFileName = serializers.CharField(required=False, max_length=64, allow_null=True, allow_blank=True)
    submitUserId = CustomUserSerializer(required=False, read_only=True)

    class Meta:
        model = Submit
        fields = '__all__'
