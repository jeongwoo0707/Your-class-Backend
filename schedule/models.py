from django.db import models
from django.conf import settings
from accounts.models import CustomUser
from assignment.models import Assignment

# Schedule models

class Schedule(models.Model):
    userId = models.ForeignKey(CustomUser, on_delete = models.CASCADE)

    class Meta:
        db_table = 'Schedule'
