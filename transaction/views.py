from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin, AictiveInstitutionRequiredMixin
from django.contrib import messages
from django.core import serializers
import json
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from applicant.models import ApplicantPrevEducation, ApplicantProfile
from applicant.forms import ApplicantProfileForm, ApplicantPrevEducationForm, ApplicantPrevEducationFormSet

from institution.models import InstitutionProfile, AdmissionSession, InstitutionSubject

from institution.forms import AdmissionSessionForm, InstitutionSubjectForm

from transaction.models import InstitutionTransactionMethod, ApplicationPayment
from transaction.forms import InstitutionTransactionMethodForm, ApplicationPaymentForm

from applications.models import Application
from applications.forms import ApplicationForm

from django.views import View, generic

# Create your views here.


class TransactionDetailsView(AictiveApplicantRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        transaction_id = kwargs.get('transaction_id')
        transaction_details = InstitutionTransactionMethod.objects.filter(
            id=transaction_id)
        data = serializers.serialize('json', transaction_details)
        return HttpResponse(data, content_type='application/json')


class TransactionMethodView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = InstitutionTransactionMethod
    paginate_by = 10
    context_object_name = 'all_transaction_method'
    template_name = 'institution/transaction/all_transaction_method.html'

    def get_queryset(self):
        try:
            qs = InstitutionTransactionMethod.objects.select_related('institute').filter(
                institute=self.request.user.user_institute).only("institute__institute_name", "method_name", "account_number")
        except Exception as e:
            qs = None
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Transaction Method'
        return context


class AddTransactionMethodView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.CreateView):
    model = InstitutionTransactionMethod
    form_class = InstitutionTransactionMethodForm
    template_name = 'institution/transaction/create_transaction_method.html'
    success_message = "Transaction Method was created successfully"
    success_url = reverse_lazy('transaction:transaction_method')

    def get_context_data(self, **kwargs):
        context = super(AddTransactionMethodView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Create Transaction Method'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        return super(AddTransactionMethodView, self).form_valid(form)


class EditTransactionMethodView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.UpdateView):
    model = InstitutionTransactionMethod
    context_object_name = 'transaction_method'
    form_class = InstitutionTransactionMethodForm
    template_name = 'institution/transaction/update_transaction_method.html'
    success_message = "Transaction Method was updated successfully"
    success_url = reverse_lazy('transaction:transaction_method')

    def get_context_data(self, **kwargs):
        context = super(EditTransactionMethodView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Update Transaction Method'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        return super(EditTransactionMethodView, self).form_valid(form)


class DeleteTransactionMethodView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.DeleteView):
    model = InstitutionTransactionMethod
    template_name = 'institution/transaction/delete_transaction_method.html'
    success_message = "Transaction Method was deleted successfully"
    success_url = reverse_lazy('transaction:transaction_method')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Transaction Method'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteTransactionMethodView, self).delete(request, *args, **kwargs)


class ApplicantPaymentListView(AictiveApplicantRequiredMixin, generic.ListView):
    model = ApplicationPayment
    context_object_name = 'payment_list'
    template_name = 'applicant/transaction/payment_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = ApplicationPayment.objects.select_related("application__applicant", "application__subject", "institute").filter(owner=self.request.user).only(
            "application__applicant__student_name", "institute__institute_name", "application__level", "application__subject__subject_name", "institute__application_fee", "transaction_number", "status", "created_at")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Applicant Payment List'
        return context


class PayApplicationFeeView(AictiveApplicantRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        application_id = kwargs.get('application_id')
        institute_id = kwargs.get('institute_id')

        institute_obj = get_object_or_404(InstitutionProfile, id=institute_id)
        transaction_method = InstitutionTransactionMethod.objects.filter(
            institute=institute_obj)

        application_payment_form = ApplicationPaymentForm(
            transaction_method=transaction_method)

        context = {
            'title': 'Payment',
            'application_id': application_id,
            'institute_id': institute_id,
            'institute_obj': institute_obj,
            'application_payment_form': application_payment_form
        }

        return render(request, 'applicant/transaction/pay_fee.html', context)

    def post(self, request, *args, **kwargs):
        application_id = kwargs.get('application_id')
        institute_id = kwargs.get('institute_id')
        institute_obj = get_object_or_404(InstitutionProfile, id=institute_id)

        transaction_method = InstitutionTransactionMethod.objects.filter(
            institute=institute_obj)
        application_payment_form = ApplicationPaymentForm(request.POST,
                                                          transaction_method=transaction_method)
        if application_payment_form.is_valid():
            instance = application_payment_form.save(commit=False)
            instance.application = get_object_or_404(
                Application, id=application_id)
            instance.owner = request.user
            instance.institute = institute_obj
            instance.save()
            messages.success(request, 'Application Fee Is Successfully Paid')
            return redirect('applications:application_list')
        else:
            context = {
                'title': 'Payment',
                'application_id': application_id,
                'institute_id': institute_id,
                'institute_obj': institute_obj,
                'application_payment_form': application_payment_form
            }

            return render(request, 'applicant/transaction/pay_fee.html', context)


class InstitutePaymentListView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = ApplicationPayment
    context_object_name = 'payment_list'
    template_name = 'institution/transaction/payment_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = ApplicationPayment.objects.select_related("application__applicant", "application__subject", "institute").filter(
            institute=self.request.user.user_institute).only("application__applicant__student_name", "institute__institute_name", "application__level", "application__subject__subject_name", "institute__application_fee", "transaction_number", "status", "created_at", "application__applicant__contact_number")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Payment List'
        return context


class InstitutePaymentCheckView(AictiveInstitutionRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        status = request.POST.get('status')

        if status == '':
            messages.error(request, ('Please Input All The Fields'))
            return redirect('transaction:institute_payment_list')
        else:
            payment_id = kwargs.get('id')
            application_payment = get_object_or_404(
                ApplicationPayment, id=payment_id)
            application_payment.status = status
            application_payment.save()
            messages.success(request, ('Withdraw Updated Successfully'))
            return redirect('transaction:institute_payment_list')
