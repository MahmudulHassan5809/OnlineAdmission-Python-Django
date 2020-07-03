from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import InstitutionTransactionMethod, ApplicationPayment


class InstitutionTransactionMethodForm(ModelForm):
    class Meta:
        model = InstitutionTransactionMethod
        exclude = ('institute',)


class ApplicationPaymentForm(ModelForm):
    class Meta:
        model = ApplicationPayment
        exclude = ('application', 'owner', 'institute',
                   'status', 'completed', 'cancel', 'pending',)

    def __init__(self, *args, **kwargs):
        self.transaction_method = kwargs.pop('transaction_method', None)
        super(ApplicationPaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'] = forms.ModelChoiceField(
            queryset=self.transaction_method)
