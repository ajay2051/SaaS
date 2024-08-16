from typing import Any

from django.core.management import BaseCommand

from subscriptions.models import Subscription


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        print("Hello World")
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            for group in obj.groups.all():
                group.permissions.set(obj.permissions.all())
                for perm in obj.permissions.all():
                    group.permissions.add(perm)
            print(obj.group.all())
            print(obj.permissions.all())