from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models.signals import post_save

from helpers.billing import create_customer, create_product

User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True


class Subscription(models.Model):
    """
    Subscription = Stripe Model
    """
    name = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    permissions = models.ManyToManyField(Permission, null=True, blank=True, limit_choices_to={'content_type__app_label': 'subscriptions'})
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        permissions = (
            ("advanced", "Advanced Permissions"),
            ("pro", "Pro Permissions"),
            ("basic", "Basic Permissions"),
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.stripe_id:
                    stripe_id = create_product(name=self.name, raw=False)
                    self.stripe_id = stripe_id
        super().save(*args, **kwargs)


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
    groups_id = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list('group__id', flat=True)
        subs_groups_set = set(subs_groups)
        # group_ids = groups_ids.values_list('id', flat=True)
        current_groups = user.groups.all().values_list('id', flat=True)
        group_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - subs_groups_set
        final_group_ids = list(group_ids_set | current_groups_set)
        user.groups.set(final_group_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)
