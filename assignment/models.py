from django.db import models
from django.conf import settings
from datetime import datetime
from uuid import uuid4
from subject.models import Subject
from accounts.models import CustomUser

# assignment model
def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file/', ymd_path, uuid_name])

class Assignment(models.Model):
    subjectId = models.ForeignKey(Subject, on_delete = models.CASCADE)
    assignmentName = models.CharField(max_length=255)
    assignmentDetail = models.TextField(null=True)
    assignmentFile = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    assignmentFileName = models.CharField(max_length=64, null=True, blank=True, verbose_name='첨부파일명')
    assignmentUpdateDate = models.DateTimeField(auto_now_add=True)
    assignmentDueDate = models.DateTimeField()
    class Meta:
        db_table = 'Assignment'

class Submit(models.Model):
    assignmentId = models.ForeignKey(Assignment, on_delete = models.CASCADE)
    submitUpdateDate = models.DateTimeField(auto_now_add=True)
    submitDetail = models.TextField(null=True)
    submitFile = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    submitFileName = models.CharField(max_length=64, null=True, blank=True, verbose_name='첨부파일명')
    submitUserId = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null =True)
    class Meta:
        db_table = 'Submit'