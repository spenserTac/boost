from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from django.contrib.auth.models import User



@receiver(post_save, sender=User)
def new_user_profile_creation(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('----- instance ----', instance, '---- type ----', type(instance))

@receiver(post_save, sender=User)
def profile_update(sender, instance, created, **kwargs):
    if created == 'False':
        instance.Profile.save()
