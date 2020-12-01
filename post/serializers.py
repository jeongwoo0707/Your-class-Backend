from django.conf import settings
# Rest Framework Serializers
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import Post, Comment
from accounts.serializers import CustomUserSerializer
from subject.serializers import SubjectSerializer

class PostSerializer(serializers.ModelSerializer):
    isNotice = serializers.BooleanField(default=True)
    postUpdateDate = serializers.DateTimeField(required=False)
    postUserId = CustomUserSerializer(read_only=True, required=False)
    postDetail = serializers.CharField()
    postName = serializers.CharField(max_length=255)
    postSubjectId = SubjectSerializer(read_only=True, required=False)
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    commentPostId = PostSerializer(read_only=True, required=False)
    commentDetail = serializers.CharField()
    commentUserId = CustomUserSerializer(read_only=True, required=False)
    commentUpdateDate = serializers.DateTimeField(required=False)
    class Meta:
        model = Comment
        fields = '__all__'