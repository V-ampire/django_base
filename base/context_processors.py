from django.conf import settings


def ajax_api_domen(request):
    return {'ajax_api_domen': settings.AJAX_API_DOMEN}