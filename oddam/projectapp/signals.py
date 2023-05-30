from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import models
from django.dispatch.dispatcher import receiver


@receiver(models.signals.pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.is_superuser:
        superusers = 0
        for user in User.objects.all():
            if instance == user:
                raise PermissionDenied
            if user.is_superuser:
                superusers += 1
        if superusers == 1:
            raise PermissionDenied
