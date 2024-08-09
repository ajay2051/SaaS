from django.db import models


class Subscription(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        permissions = (
            ("advanced", "Advanced Permissions"),
            ("pro", "Pro Permissions"),
            ("basic", "Basic Permissions"),
        )
