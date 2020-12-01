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

from .models import CustomUser
from assignment.models import Assignment, Submit
from subject.models import Subject, Enroll
from subject.serializers import SubjectSerializer, EnrollSerializer
from assignment.serializers import AssignmentSerializer, SubmitSerializer 
from accounts.serializers import CustomUserSerializer 
from django.shortcuts import get_object_or_404

class EnrollAPIView(APIView):
    def get_object(self):
        try:
            return Enroll.objects.filter(userId = self.request.user)
        except Enroll.DoesNotExist:
            raise Http404
            
    def get(self, request, format=None):
        enroll = self.get_object()
        serializer = EnrollSerializer(enroll, many=True)
        return Response(serializer.data)

class AssignmentAPIView(APIView):
    def get_object(self, subjectId):
        try:
            return Assignment.objects.filter(subjectId__id = subjectId)
        except Assignment.DoesNotExist:
            raise Http404
    
    def get(self, request, subjectId, format=None):
        assignment = self.get_object(subjectId)
        serializer = AssignmentSerializer(assignment, many=True)
        return Response(serializer.data)

