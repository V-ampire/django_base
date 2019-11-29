from django.utils.http import is_safe_url, urlunquote, urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature
from django.utils.encoding import force_bytes, force_text
from datetime import timedelta


def get_next_url(request):
    """
        Return previous URL.
        For example to redirect user back to page where he logged in.
    """
    next = request.META.get('HTTP_REFERER')
    if next:
        next = urlunquote(next) # HTTP_REFERER may be encoded.
    if not is_safe_url(url=next, allowed_hosts=request.get_host()):
        next = settings.LOGIN_REDIRECT_URL
    return next


def get_client_ip(request):
    """
        Получение IP адреса пользователя из запроса
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_temp_url_token(user):
    signer = TimestampSigner(salt='my_auth')
    value = signer.sign(user.username)
    token = urlsafe_base64_encode(force_bytes(value))
    return token


def check_temp_url_token(token, seconds=None):
    """If token not expired return user.username, else return None"""
    if not seconds:
        seconds = settings.REGISTER_TIMEOUT
    signer = TimestampSigner(salt='my_auth')
    value = force_text(urlsafe_base64_decode(token))
    try:
        return signer.unsign(value, max_age=timedelta(seconds=seconds))
    except SignatureExpired:
        return
    except BadSignature:
        return