from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import AdmissionSession


class AdmissionSessionForm(ModelForm):
    class Meta:
        model = AdmissionSession
        exclude = ('institute',)
