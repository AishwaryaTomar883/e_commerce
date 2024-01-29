from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

ROLES = ["Customer", "Seller"]


class Command(BaseCommand):
    help = "Create roles"

    def handle(self, *args, **options):
        for role in ROLES:
            # create or get group
            group, created = Group.objects.get_or_create(name=role)
            self.stdout.write(
                self.style.SUCCESS(f"{role} group created successfully")
                    )
