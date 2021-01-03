from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from metrics.models import SignUpMetricModel
from django.contrib.auth.models import User



@receiver(post_save, sender=User)
def new_user_profile_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        SignUpMetricModel.objects.create(user=instance)


@receiver(post_save, sender=User)
def profile_update(sender, instance, created, **kwargs):
    if created == 'False':
        instance.Profile.save()
