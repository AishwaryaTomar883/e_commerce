from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model representing a user in the system."""

    email = models.EmailField(_("email address"), unique=True)

    def save(self, *args, **kwargs):
        """
        Saves the user object.
        This method sets the username field to the user's email address before saving the object.
        """
        self.username = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Returns a string representation of the user.
        Returns:
            str: The email address of the user.
        """
        return self.email
