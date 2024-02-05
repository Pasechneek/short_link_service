import logging
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import AddNewLinkForm
from django.template import loader
from .models import ShortLinkService
from .serializers import ShortLinkSerializer
from .services import _increase_counter, _normalize_url, _short_generator, _db_get_or_create
from rest_framework import generics


class ShortLincAPIView(generics.ListAPIView):
    queryset = ShortLinkService.objects.all()
    serializer_class = ShortLinkSerializer


def index(request):
    """main page view"""
    template = loader.get_template('homepage.html')
    queries = ShortLinkService.objects.all().order_by('-count')
    context = {
        'queries': queries,
    }
    return HttpResponse(template.render(context, request))


def add_new_link(request):
    """Получает данные из формы, записывает их в таблицу links и вызывает вью result"""
    if request.method == 'POST':
        form = AddNewLinkForm(request.POST)
        if form.is_valid():
            the_origin_link = form.cleaned_data.get('origin_link')
            try:
                the_origin_link = _normalize_url(the_origin_link)
                url_validator = URLValidator()
                url_validator.__call__(the_origin_link)
                generated_short_link = _short_generator(the_origin_link)
                _db_get_or_create(generated_short_link, the_origin_link)
                return HttpResponseRedirect(f"result/{generated_short_link}")
            except ValidationError as e1:
                messages.error(request, "Error I: Wrong link")
                logging.exception(e1)
            except Exception as e2:
                messages.error(request, "Error II: Wrong link")
                logging.exception(e2)
    else:
        form = AddNewLinkForm()
    return render(request, 'add_new_link.html', {'form': form})


def show_result(request, short_link):
    """Показывает результат обработки ссылки"""
    the_origin_link = ShortLinkService.objects.filter(short_link=short_link).first()
    try:
        the_origin_link = redirect(_normalize_url(f"{the_origin_link}"))
        context = {
            'short_link': short_link,
            'the_origin_link': the_origin_link,
            'absolute_short_link': request.build_absolute_uri(
                reverse('short_link_redirect', kwargs={'short_link': short_link}))
        }
    except Exception as e:
        messages.error(request, "Error III: Wrong link")
        logging.exception(e)
        context = {
            'messages': messages,
            'short_link': short_link,
            'the_origin_link': the_origin_link,
            'absolute_short_link': request.build_absolute_uri(
                reverse('short_link_redirect', kwargs={'short_link': short_link}))
        }
    return render(request, 'result.html', context)


def shot_link_redirect(request, short_link):
    """Осуществляет редирект на оригинальную ссылку"""
    if short_link == 'favicon.ico':
        return render(request, 'add_new_link.html')
    else:
        the_origin_link = ShortLinkService.objects.filter(short_link=short_link).first()

        if the_origin_link:
            _increase_counter(request, short_link)
            the_origin_link = _normalize_url(f"{the_origin_link}")
            return redirect(the_origin_link)
        else:
            return render(request, 'add_new_link.html')
