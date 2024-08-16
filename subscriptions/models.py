from django.contrib.auth.models import Group, Permission
from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    permissions = models.ManyToManyField(Permission, null=True, blank=True, limit_choices_to={'content_type__app_label': 'subscriptions'})

    class Meta:
        permissions = (
            ("advanced", "Advanced Permissions"),
            ("pro", "Pro Permissions"),
            ("basic", "Basic Permissions"),
        )
