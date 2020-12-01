import traceback
import string
import random
from rest_framework import (generics, permissions, status, )
from rest_framework import mixins,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from drf_multiple_model.views import ObjectMultipleModelAPIView

from .models import Subject, Enroll
from .serializers import SubjectSerializer, CustomUserSerializer, EnrollSerializer, EnrollSubjectSerializer

# 과목의 Create를 위한 View
class CreateSubjectApiView(generics.CreateAPIView):
    """ 새로운 과목을 생성한다."""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    def create(self, request, *args, **kwargs):
        """ 에러 발생 시, 해당 항목을 출력하도록 변경 """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(subjectInstructorId = self.request.user, invitationCode = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)))
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 과목의 RUD를 위한 View
class SubjectView(APIView):
    # 입력받은 pk에 해당하는 subject을 받아옴.
    def get_object(self, pk):
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            raise Http404
    # 과목의 정보를 출력한다.
    def get(self, request, pk, format=None):
        subject = self.get_object(pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)
    # 과목의 정보를 수정한다.
    def put(self, request, pk, format=None):
        subject = self.get_object(pk)
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 과목을 삭제한다.
    def delete(self, request, pk, format=None):
        subject = self.get_object(pk)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 과목 등록을 위한 View
class InviteView(APIView):
    # 입력받은 invitationCode에 해당하는 subject를 받아옴.
    def get_object(self, invitationCode):
        try:
            return Subject.objects.get(invitationCode=invitationCode)
        except Subject.DoesNotExist:
            raise Http404
    # 과목의 정보를 출력한다.
    def get(self, request, invitationCode, format=None):
        subject = self.get_object(invitationCode)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

# user가 수강하고 있는 과목을 출력하기 위한 View
class EnrollViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = EnrollSerializer
    queryset = Enroll.objects.all()

    def get_queryset(self):
        return self.queryset.filter(userId=self.request.user)

class EnrollView(APIView):
    # 입력받은 invitationCode에 해당하는 subject를 받아옴.
    def get_object(self, invitationCode):
        try:
            return Subject.objects.get(invitationCode=invitationCode)
        except Subject.DoesNotExist:
            raise Http404
    
    def get_enroll(self, subjectId, userId):
        try:
            return Enroll.objects.get(userId__id = userId, subjectId__id =subjectId)
        except Enroll.DoesNotExist:
            raise Http404

    # 사용하고 있는 user를 과목 수강생에 추가함.
    def post(self, request, invitationCode, format=None):
        subject = self.get_object(invitationCode)
        serializer = EnrollSerializer(data= request.data)
        queryset = Enroll.objects.filter(userId = self.request.user, subjectId = subject)
        if serializer.is_valid():
            if queryset.exists():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(userId = self.request.user, subjectId = subject)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, subjectId, userId, format=None):
        enroll = self.get_enroll(subjectId, userId)
        enroll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 과목의 invitationCode를 reset하기 위한 view
class ResetInvitationView(APIView):
    def get_object(self, pk):
        try:
            return Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        subject = self.get_object(pk)
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(invitationCode = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 과목 수강생 목록을 위한 View
class SubjectEnrollView(generics.ListAPIView):
    serializer_class = EnrollSerializer
    queryset = Enroll.objects.all()
    filter_backends = (DjangoFilterBackend,)
    
    def get_queryset(self):
        Id = self.request.query_params.get('Id',None)
        return Enroll.objects.filter(subjectId__id=Id)
