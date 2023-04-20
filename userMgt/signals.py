from django.db.models.signals import post_save
from .models import User,Profile
from django.dispatch import receiver

@receiver(post_save,sender=User)
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

