from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import AdmissionSession, InstitutionTransactionMethod


class AdmissionSessionForm(ModelForm):
    class Meta:
        model = AdmissionSession
        exclude = ('institute',)


class InstitutionTransactionMethodForm(ModelForm):
    class Meta:
        model = InstitutionTransactionMethod
        exclude = ('institute',)