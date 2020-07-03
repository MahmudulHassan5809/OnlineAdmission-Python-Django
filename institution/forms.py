from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import AdmissionSession, InstitutionSubject, InstitutionProfile


class AdmissionSessionForm(ModelForm):
    class Meta:
        model = AdmissionSession
        exclude = ('institute',)


class InstitutionSubjectForm(ModelForm):
    class Meta:
        model = InstitutionSubject
        exclude = ('institute',)
