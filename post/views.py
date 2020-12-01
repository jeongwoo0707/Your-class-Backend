import traceback
from rest_framework import (generics, permissions, status, )
from rest_framework import mixins,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from drf_multiple_model.views import ObjectMultipleModelAPIView

from .models import Post, Comment
from subject.models import Subject
from .serializers import PostSerializer, CommentSerializer
from accounts.serializers import CustomUserSerializer
from subject.serializers import SubjectSerializer

class CreateNoticeApiView(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self, subjectId):
        try:
            return Subject.objects.get(id= subjectId)
        except Subject.DoesNotExist:
            raise Http404

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        subject = self.get_object(request.POST.get('classId'))
        if serializer.is_valid():
            serializer.save(postUserId = self.request.user, postSubjectId = subject)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateQuestionApiView(generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self, subjectId):
        try:
            return Subject.objects.get(id=subjectId)
        except Subject.DoesNotExist:
            raise Http404

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        subject = self.get_object(request.POST.get('classId'))
        if serializer.is_valid():
            serializer.save(postUserId = self.request.user, postSubjectId = subject, isNotice= False)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostApiListView(APIView):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self, subjectId):
        try:
            return self.queryset.filter(postSubjectId__id=subjectId).order_by('-postUpdateDate')[:3]
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, subjectId, format=None):
        post = self.get_object(subjectId)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

class NoticeApiListView(APIView):
    
    def get_object(self, subjectId):
        try:
            return Post.objects.filter(postSubjectId__id = subjectId, isNotice = True)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, subjectId, format=None):
        post = self.get_object(subjectId)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
    
class QuestionApiListView(APIView):

    def get_object(self, subjectId):
        try:
            return Post.objects.filter(postSubjectId__id = subjectId, isNotice = False)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, subjectId, format=None):
        post = self.get_object(subjectId)
        serializer = PostSerializer(post, many= True)
        return Response(serializer.data)

class PostApiDetailView(APIView):
    
    def get_object(self, postId):
        try:
            return Post.objects.get(id= postId)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, postId, format=None):
        post = self.get_object(postId)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, postId, format=None):
        post = self.get_object(postId)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, postId, format=None):
        post = self.get_object(postId)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateCommentApiView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_object(self, postId):
        try:
            return Post.objects.get(id= postId)
        except Post.DoesNotExist:
            raise Http404

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        post = self.get_object(request.POST.get('postId'))
        if serializer.is_valid():
            serializer.save(commentUserId = self.request.user, commentPostId = post)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentApiListView(APIView):
    
    def get_object(self, postId):
        try:
            return Comment.objects.filter(commentPostId__id = postId)
        except Comment.DoesNotExist:
            raise Http404
    
    def get(self, request, postId, format=None):
        comment = self.get_object(postId)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

class CommentDetailView(APIView):

    def get_object(self, commentId):
        try:
            return Comment.objects.get(id = commentId, commentUserId = self.request.user)
        except Comment.DoesNotExist:
            raise Http404
    
    def put(self, request, commentId, format=None):
        comment = self.get_object(commentId)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, commentId, format=None):
        comment = self.get_object(commentId)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


