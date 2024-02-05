from django import forms
from .models import *


class AddNewLinkForm(forms.Form):
    origin_link = forms.CharField(max_length=255, label='Ваша ссылка')
    # short_link = forms.CharField(max_length=6)
