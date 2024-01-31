from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model

from utils.constants import ProductImageConstants, CarouselImageConstants


def get_model(app_label: str, model_name: str) -> Model:
    """This function will return model object
    :param: app_label (name of app label)
    :param: model_name (name of model)
    :returns: Model Object i.e
            <class 'user.models.User'>
    """
    try:
        return apps.get_model(app_label, model_name)
    except ValueError:
        raise ImproperlyConfigured(
            f"Model {model_name} must be in app directory {app_label}"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"App label {app_label} must be defined in project directory"
        )


def normalize_email(email: str) -> str:
    """
    Normalize the given email address.

    This function takes an email address as input and performs normalization by stripping leading and trailing whitespace
    and converting the email address to lowercase.

    Args:
        email (str): The email address to normalize.

    Returns:
        str: The normalized email address.
    """
    return email.strip().lower()


def product_image_upload_path(instance, filename) -> str:
    """Function to create an upload path for product image."""
    return f"{ProductImageConstants.PRODUCT_IMAGE_PATH}/{filename}"


def carousel_image_upload_path(instance, filename) -> str:
    """Function to create an upload path for carousel image."""
    return f"{CarouselImageConstants.CAROUSEL_IMAGE_PATH}/{filename}"
