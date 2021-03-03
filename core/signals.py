# django imports
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

# third-party imports

# local imports
from .models import *


User = get_user_model()

@receiver(post_save, sender=User)
def create_profile_receiver(sender, instance, created, **kwargs):
    print(kwargs, sender)
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def update_user_receiver(sender, instance, created, **kwargs):
    print(kwargs, sender)
    if created:
        instance.user.save()

