import logging
from hashlib import sha256
from django.contrib import messages

from .models import ShortLinkService


def _short_generator(the_origin_link):
    """Генерирует короткую ссылку"""
    if the_origin_link == '':
        return ''
    if the_origin_link is None:
        return ''
    short_link = the_origin_link.encode('utf-8')
    short_link = sha256(short_link).hexdigest()[-6:]
    return short_link


def _normalize_url(url):
    """Осуществляет нормализацию URL"""
    url = str(url)
    prefix = 'https://'
    if url[0:8] == prefix:
        return url
    else:
        if url[0:7] == 'http://':
            return prefix + url[7:]
        else:
            return prefix + url


def _increase_counter(request, short_link):
    """Считает количество переходов по ссылке"""
    if request and short_link:
        try:
            query = ShortLinkService.objects.get(short_link=short_link)
            query.count = query.count + 1
            query.save()
            return query.count
        except Exception as e:
            logging.exception(e)
            messages.error(request, "short link not found, when counter increases ")


def _db_get_or_create(generated_short_link, the_origin_link) -> None:
    """Ищет в базе пару короткой и длинной ссылки. Если не нашёл - записывает их"""
    ShortLinkService.objects.get_or_create(short_link=generated_short_link,
                                           defaults=dict(
                                               short_link=generated_short_link,
                                               origin_link=the_origin_link))
