from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db import models
from django.db.models.signals import post_save

from helpers.billing import create_customer, create_price, create_product

User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True


class Subscription(models.Model):
    """
    Subscription = Stripe Subscription
    """
    name = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=True)
    group = models.ManyToManyField(Group, null=True, blank=True)
    permissions = models.ManyToManyField(Permission, null=True, blank=True, limit_choices_to={'content_type__app_label': 'subscriptions'})
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    featured = models.BooleanField(default=True, help_text="Featured on Django Pricing Page")


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

class SubscriptionPrice(models.Model):
    """
    Subscription Price = Stripe Price
    """

    class IntervalChoices(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Monthly'
        WEEKLY = 'WEEKLY', 'Weekly'
        YEARLY = 'YEARLY', 'Yearly'
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    interval = models.CharField(max_length=120, default=IntervalChoices.WEEKLY, choices=IntervalChoices.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    order = models.IntegerField(default=-1, help_text="Ordering on Django pricing Page")
    featured = models.BooleanField(default=True, help_text="Featured on Django Pricing Page")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ['order', 'timestamp', '-updated']

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def stripe_price(self) -> int:
        return Decimal(self.price) * 100

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id

    def save(self, *args, **kwargs):
        if self.stripe_id is None and self.product_stripe_id is not None:
            import stripe
            stripe.api_key = 'sk_test_s15s1cs5c15a4sdxa1xwfw'
            stripe_id = create_price(currency=self.stripe_currency, unit_amount=self.stripe_price, recurring=self.interval,
                                 product=self.product_stripe_id)
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)
        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription=self.subscription,
                interval=self.interval,
            ).exclude(id=self.id)
            qs.update(featured=False)


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
