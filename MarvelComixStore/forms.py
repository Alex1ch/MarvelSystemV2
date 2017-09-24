from django.forms import Form, ModelForm
from django import forms
from django.utils import timezone
from MarvelComixStore.models import Comic

class searchForm(Form):
    keywords = forms.CharField(max_length=100, label="Ключевые слова", required=False)
