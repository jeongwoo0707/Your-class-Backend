from django.db import models
from django.conf import settings
from accounts.models import CustomUser

# Subject models

class Subject(models.Model):
    subjectName = models.CharField(max_length=255)
    subjectTimeList = models.TextField()
    subjectInstructorId = models.ForeignKey(CustomUser,related_name = 'uid_for_instructor', on_delete = models.CASCADE)
    invitationCode = models.CharField(max_length=16, null = True)
    subjectGrade = models.IntegerField()
    subjectClass = models.IntegerField()
    class Meta:
        db_table = 'Subject'

class Enroll(models.Model):
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subjectId = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Enroll'