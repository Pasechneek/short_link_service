from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import request
from django.test import TestCase

from short_link_app.models import ShortLinkService
from short_link_app.services import _short_generator, _normalize_url, _increase_counter, _db_get_or_create


class ServicesTestCase(TestCase):
    def test_short_generator(self):
        result = _short_generator('')
        self.assertEqual('', result)

    def test_short_generator_2(self):
        result = _short_generator('https://www.google.com')
        self.assertEqual('162c09', result)

    def test_normalize_url(self):
        result = _normalize_url('www.google.com')
        self.assertEqual('https://www.google.com', result)

    def test_normalize_url_2(self):
        result = _normalize_url('http://www.google.com')
        self.assertEqual('https://www.google.com', result)

    def setUp(self) -> None:
        ShortLinkService.objects.create(short_link='162c09', origin_link='https://www.google.com')

    def test_increase_counter_2(self):
        short_link = '162c09'
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        result = _increase_counter(request, short_link)
        self.assertEqual(result, 1)

    def test_db_get_or_create(self):
        _db_get_or_create('939080', 'https://www.youtube.com')
        result = ShortLinkService.objects.get(short_link='939080')
        self.assertEqual(result.origin_link, 'https://www.youtube.com')

    def test_db_get_or_create_2(self):
        _db_get_or_create('162c09', 'http://www.google.com')
        result = ShortLinkService.objects.get(short_link='162c09')
        self.assertEqual(result.origin_link, 'https://www.google.com')
