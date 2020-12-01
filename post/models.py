from django.db import models
from django.conf import settings
from accounts.models import CustomUser
from subject.models import Subject

# Create your models here.

class Post(models.Model):
    isNotice = models.BooleanField(default=True)
    postUpdateDate = models.DateTimeField(auto_now_add=True)
    postUserId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    postDetail = models.TextField()
    postName = models.CharField(max_length=255)
    postSubjectId = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Post'

class Comment(models.Model):
    commentPostId = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentDetail = models.TextField()
    commentUserId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    commentUpdateDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comment'