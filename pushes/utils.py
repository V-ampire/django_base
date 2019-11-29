from django.conf import settings
import json
from pywebpush import webpush
from .models import Subscription


def send_push(sub, message):
    """
        Send push notification
        sub - Subscription object
        message - {
            "head": ...,
            "body": ...
        }
    """
    res = webpush(
        subscription_info=sub.subscription,
        data=json.dumps(message),
        vapid_private_key=settings.VAPID_PRIVATE_KEY,
        vapid_claims={
                "sub": "mailto:{}".format(settings.VAPID_ADMIN_EMAIL),
            }
    )
    return res