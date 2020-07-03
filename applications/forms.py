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
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = InstitutionSubject.objects.none()

        if 'institute' in self.data:
            try:
                institute_id = int(self.data.get('institute'))
                self.fields['subject'].queryset = InstitutionSubject.objects.filter(
                    institute_id=institute_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            print('0kkkkkkkkkkkkkkkkkk')
            self.fields['subject'].queryset = self.instance.user_institute.institute_subjects


class ApplicationPaymentForm(ModelForm):
    class Meta:
        model = ApplicationPayment
        exclude = ('application',)

    def __init__(self, *args, **kwargs):
        self.transaction_method = kwargs.pop('transaction_method', None)
        super(ApplicationPaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'] = forms.ModelChoiceField(
            queryset=self.transaction_method)
