from django.contrib.auth.models import Group, Permission
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL


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

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

def user_sub_post_save(sender, instance, created, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups = subscription_obj.groups.all()
    user.groups.set(groups)
post_save.connect(user_sub_post_save, sender=UserSubscription)
