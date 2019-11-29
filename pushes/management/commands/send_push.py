from django.core.management.base import BaseCommand
from pushes.models import Subscription
from pushes.utils import send_push

import json


class Command(BaseCommand):
    help = 'Send push notifications'

    def handle(self, *args, **kwargs):
        for sub in Subscription.objects.all():
            vacancies = sub.user.vacancies_list
            print(vacancies.vacancies)
            message = {
                "head": "test notification",
                "body": vacancies.vacancies
            }
            res = send_push(sub, json.dumps(message, ensure_ascii=False))
            print(res)
