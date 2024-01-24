from django.conf import settings


def debug_state(request):
    return {'DEBUG': settings.DEBUG}
