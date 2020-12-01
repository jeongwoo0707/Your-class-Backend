from django.db.models.signals import post_save
from django.dispatch import receiver
from subject.models import Subject, Enroll

@receiver(post_save, sender = Subject)
def Subject_post_save (sender, instance, **kwargs):
    if kwargs['created']:
        Enroll.objects.create(subjectId = instance, userId = instance.subjectInstructorId)
        print("enroll created ")