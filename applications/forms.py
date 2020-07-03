from django import forms
from django.forms import ModelForm
from .models import Application, ApplicationPayment
from institution.models import InstitutionProfile, InstitutionSubject


class ApplicationForm(ModelForm):
    institute = forms.ModelChoiceField(
        queryset=InstitutionProfile.objects.filter(active=True))

    class Meta:
        model = Application
        exclude = ('owner', 'applicant', 'status', 'paid',)

    def __init__(self, *args, **kwargs):
        self.institute_subject = kwargs.pop('institute_subject', None)
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = InstitutionSubject.objects.none()


class ApplicationPaymentForm(ModelForm):
    class Meta:
        model = ApplicationPayment
        exclude = ('application',)

    def __init__(self, *args, **kwargs):
        self.transaction_method = kwargs.pop('transaction_method', None)
        super(ApplicationPaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'] = forms.ModelChoiceField(
            queryset=self.transaction_method)
