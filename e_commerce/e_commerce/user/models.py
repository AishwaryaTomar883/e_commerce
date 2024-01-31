from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
)

from utils.utils import product_image_upload_path, carousel_image_upload_path


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


class BaseMasterModel(ActivatorModel, TimeStampedModel):
    """
    Abstract base model for master models.
    This model serves as an abstract base model for other master models and includes the
    ActivatorModel and TimeStampedModel as parent classes.
    """

    class Meta:
        abstract = True


class Category(BaseMasterModel):
    """model for storing categories"""
    name = models.CharField(max_length=150, null=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the category name.
        Returns:
            str: The name of the category.
        """
        return self.name


class Product(BaseMasterModel):
    """model for storing products"""
    name = models.CharField(max_length=150, null=True)
    price = models.IntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    image = models.ImageField(upload_to=product_image_upload_path, null=True)


class CarouselImage(BaseMasterModel):
    """model for storing carousel images"""
    image = models.ImageField(upload_to=carousel_image_upload_path, null=True)
