from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from schedule.models import Schedule


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    print("Is Created: ", created)

    if created:
        Profile.objects.create(user=instance,
                               nickname=instance.name)
        Schedule.objects.create(userId=instance)
