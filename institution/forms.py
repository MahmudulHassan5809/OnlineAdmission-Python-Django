from django import forms
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import get_user_model
from .models import AdmissionSession, InstitutionSubject, InstitutionProfile, InstituteInstruction, Subscription


class DateInput(forms.DateInput):
    input_type = 'date'


class AdmissionSessionForm(ModelForm):
    class Meta:
        model = AdmissionSession
        exclude = ('institute',)
        widgets = {
            'end_time': DateInput(),
        }


class InstitutionSubjectForm(ModelForm):
    class Meta:
        model = InstitutionSubject
        exclude = ('institute',)


class InstituteSearchForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=InstitutionProfile.objects.filter(active=True).values_list('institute_city', flat=True).distinct())
    subject = forms.ModelChoiceField(
        queryset=InstitutionSubject.objects.all().values_list('subject_name', flat=True).distinct())


class InstituteInstructionForm(ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = InstituteInstruction
        exclude = ('institute',)


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        exclude = ('institute',)
        widgets = {
            'user_email': forms.TextInput(attrs={'placeholder': 'Your Email'}),
        }

    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['user_email'].label = ""
