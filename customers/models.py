from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user}"
