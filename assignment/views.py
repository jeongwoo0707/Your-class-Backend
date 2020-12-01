import traceback
import urllib
import os
import mimetypes
from rest_framework import (generics, permissions, status, )
from rest_framework import mixins,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404,HttpResponse
from rest_framework.viewsets import ViewSet

from drf_multiple_model.views import ObjectMultipleModelAPIView

from .models import Assignment, Submit, Subject
from .serializers import SubjectSerializer, AssignmentSerializer, SubmitSerializer, CustomUserSerializer
from django.shortcuts import get_object_or_404

def assignment_download_view(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    url = assignment.assignmentFile.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(assignment.assignmentFileName.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404

def submit_download_view(request, pk):
    submit = get_object_or_404(Submit, pk=pk)
    url = submit.submitFile.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(submit.submitFileName.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404

class CreateAssignmentApiView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
        
    def list(self, request):
        return Response("GET API")

    def get_object(self, subjectId):
        try:
            return Subject.objects.get(id=subjectId)
        except Subject.DoesNotExist:
            raise Http404
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        file_uploaded = request.FILES.get('assignmentFile')
        if file_uploaded is not None:
            filename = request.FILES['assignmentFile'].name
        subject = self.get_object(request.POST.get('classId'))
        if serializer.is_valid():
            if file_uploaded is None:
                serializer.save(subjectId = subject)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            serializer.save(subjectId = subject, assignmentFile = file_uploaded, assignmentFileName = filename)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignmentApiView(APIView):

    def get_object(self, subjectId):
        try:
            return Assignment.objects.filter(subjectId__id=subjectId)
        except Assignment.DoesNotExist:
            raise Http404
    
    def get(self, request, subjectId, format=None):
        assignment = self.get_object(subjectId)
        serializer = AssignmentSerializer(assignment, many =True)
        return Response(serializer.data)

class AssignmentDetailView(APIView):

    def get_object(self, assignmentId):
        try:
            return Assignment.objects.get(id=assignmentId)
        except Assignment.DoesNotExist:
            raise Http404
    
    def get(self, request, assignmentId, format=None):
        assignment = self.get_object(assignmentId)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)
    
    def delete(self, request, assignmentId, format=None):
        assignment = self.get_object(assignmentId)
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, assignmentId, format=None):
        assignment = self.get_object(assignmentId)
        serializer = AssignmentSerializer(assignment, data=request.data, partial=True)
        file_uploaded = request.FILES.get('assignmentFile')
        if file_uploaded is not None:
            filename = request.FILES['assignmentFile'].name
        if serializer.is_valid():
            if file_uploaded is None:
                serializer.save(assignmentFile = None, assignmentFileName = None)
                return Response(serializer.data)
            serializer.save(assignmentFile = file_uploaded, assignmentFileName = filename)   
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateSubmitApiView(generics.CreateAPIView):
    serializer_class = SubmitSerializer
    queryset = Submit.objects.all()
        
    def list(self, request):
        return Response("GET API")

    def get_object(self, assignmentId):
        try:
            return Assignment.objects.get(id=assignmentId)
        except Assignment.DoesNotExist:
            raise Http404
    
    def create(self, request ,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        file_uploaded = request.FILES.get('submitFile')
        if file_uploaded is not None:
            filename = request.FILES['submitFile'].name
        assignment = self.get_object(request.POST.get('assignId'))
        if serializer.is_valid():
            if file_uploaded is None:
                serializer.save(assignmentId = assignment, submitUserId= self.request.user)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            serializer.save(assignmentId = assignment, submitUserId= self.request.user, submitFile = file_uploaded, submitFileName = filename)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubmitApiView(APIView):

    def get_object(self, assignmentId):
        try:
            return Submit.objects.filter(assignmentId__id=assignmentId)
        except Submit.DoesNotExist:
            raise Http404
    
    def get(self, request, assignmentId, format=None):
        submit = self.get_object(assignmentId)
        serializer = SubmitSerializer(submit, many =True)
        return Response(serializer.data)

class SubmitDetailView(APIView):

    def get_object(self, assignId):
        try:
            return Submit.objects.get(assignmentId__id=assignId, submitUserId = self.request.user)
        except Submit.DoesNotExist:
            raise Http404
    
    def get(self, request, assignId, format=None):
        submit = self.get_object(assignId)
        serializer = SubmitSerializer(submit)
        return Response(serializer.data)
    
    def delete(self, request, assignId, format=None):
        submit = self.get_object(assignId)
        submit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, assignId, format=None):
        submit = self.get_object(assignId)
        serializer = SubmitSerializer(submit, data=request.data, partial=True)
        file_uploaded = request.FILES.get('submitFile')
        if file_uploaded is not None:
            filename = request.FILES['submitFile'].name
        if serializer.is_valid():
            if file_uploaded is None:
                serializer.save(submitFile = None, submitFileName = None)
                return Response(serializer.data)
            serializer.save(submitFile = file_uploaded, submitFileName = filename)   
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IsSubmitView(APIView):

    def get_object(self, assignmentId):
        try:
            return Submit.objects.get(assignmentId__id = assignmentId, submitUserId = self.request.user)
        except Submit.DoesNotExist:
            return None

    def get(self, request, assignmentId, format=None):
        submit = self.get_object(assignmentId)
        if submit is None:
            return Response({
                                "assignmentId" : assignmentId,
                                "isSubmitted" : 0
                            })
        else:
            return Response({
                                "assignmentId" : assignmentId,
                                "isSubmitted" : 1
                            })

class IsSubmitListView(APIView):

    def get_object(self, assignmentId, submitUserId):
        try:
            return Submit.objects.get(assignmentId__id = assignmentId, submitUserId = submitUserId)
        except Submit.DoesNotExist:
            return None

    def get(self, request, assignmentId, submitUserId, format=None):
        submit = self.get_object(assignmentId, submitUserId)
        if submit is None:
            return Response({
                                "submitUserId" : submitUserId,
                                "isSubmitted" : 0
                            })
        else:
            return Response({
                                "submitUserId" : submitUserId,
                                "isSubmitted" : 1
                            })

class IsSubmitDetailView(APIView):

    def get_object(self, userId, assignmentId):
        try:
            return Submit.objects.get(submitUserId__id=userId, assignmentId__id=assignmentId)
        except Submit.DoesNotExist:
            raise Http404

    def get(self, request, userId, assignmentId, format=None):
        submit = self.get_object(userId, assignmentId)
        serializer = SubmitSerializer(submit)
        return Response(serializer.data)