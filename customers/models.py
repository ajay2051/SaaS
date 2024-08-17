from django.db import models
from django.conf import settings

from helpers.billing import create_customer

User = settings.AUTH_USER_MODEL

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    def save(self, *args, **kwargs):
        email = self.user.email
        if not self.stripe_id:
            if email != "" or email is not None:
                stripe_id = create_customer(email=email, raw=True)
                self.stripe_id = stripe_id
        super().save(*args, **kwargs)
