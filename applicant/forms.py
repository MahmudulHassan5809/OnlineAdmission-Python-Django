from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import ApplicantPrevEducation, ApplicantProfile
from django.contrib.auth import get_user_model


class DateInput(forms.DateInput):
    input_type = 'date'


class ApplicantProfileForm(ModelForm):
    present_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    permanent_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

    class Meta:
        model = ApplicantProfile
        exclude = ('owner',)
        widgets = {
            'birth_date': DateInput(),
        }


class ApplicantPrevEducationForm(ModelForm):
    class Meta:
        model = ApplicantPrevEducation
        fields = '__all__'


ApplicantPrevEducationFormSet = inlineformset_factory(
    ApplicantProfile, ApplicantPrevEducation, form=ApplicantPrevEducationForm, extra=1)
