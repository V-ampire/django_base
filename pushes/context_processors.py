from django.conf import settings


def push_public_vapid(request):
    return {'vapid_key': settings.VAPID_PUBLIC_KEY}