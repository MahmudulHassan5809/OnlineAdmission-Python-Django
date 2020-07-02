from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin, AictiveInstitutionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AdmissionSessionForm, InstitutionTransactionMethodForm
from django.views import View, generic
from django.contrib.auth import get_user_model
from applications.models import ApplicantPrevEducation, ApplicantProfile
from .models import InstitutionProfile, AdmissionSession, InstitutionTransactionMethod
# Create your views here.


class AdmissionSessionView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = AdmissionSession
    context_object_name = 'admission_session'
    template_name = 'institution/session/adminssion_session.html'

    def get_queryset(self):
        try:
            qs = AdmissionSession.objects.filter(
                institute=self.request.user.user_institute).first()
        except Exception as e:
            qs = None
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Admission Session'
        return context

    def render_to_response(self, context):
        try:
            qs = AdmissionSession.objects.filter(
                institute=self.request.user.user_institute).first()
        except Exception as e:
            messages.info(self.request, 'You Dont Have Any Institute')
            return redirect('accounts:login_success')
        return super().render_to_response(context)


class CreateInstitutionSession(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.CreateView):
    model = AdmissionSession
    form_class = AdmissionSessionForm
    template_name = 'institution/session/create_session.html'
    success_message = "Session was created successfully"
    success_url = reverse_lazy('institution:admission_session')

    def get_context_data(self, **kwargs):
        context = super(CreateInstitutionSession,
                        self).get_context_data(**kwargs)
        context['title'] = 'Create Admission Session'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        self.object.save()

        return super(CreateInstitutionSession, self).form_valid(form)

    def render_to_response(self, context):
        qs = AdmissionSession.objects.filter(
            institute=self.request.user.user_institute).first()
        if qs:
            messages.info(self.request, 'Please Update Previous Data')
            return redirect('institution:admission_session')
        return super().render_to_response(context)


class UpdateInstitutionSession(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.UpdateView):
    model = AdmissionSession
    form_class = AdmissionSessionForm
    context_object_name = 'admission_session'
    template_name = 'institution/session/update_session.html'
    success_message = "Session was updated successfully"
    success_url = reverse_lazy('institution:admission_session')

    def get_context_data(self, **kwargs):
        context = super(UpdateInstitutionSession,
                        self).get_context_data(**kwargs)
        context['title'] = 'Update Admission Session'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        self.object.save()

        return super(UpdateInstitutionSession, self).form_valid(form)


class DeleteInstitutionSession(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.DeleteView):
    model = AdmissionSession
    template_name = 'institution/session/delete_session.html'
    success_message = "Admission Session was deleted successfully"
    success_url = reverse_lazy('institution:admission_session')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Profile'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteInstitutionSession, self).delete(request, *args, **kwargs)


class MyInstituteView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = InstitutionProfile
    context_object_name = 'my_institute'
    template_name = 'institution/institute/my_institute.html'

    def get_queryset(self):
        qs = self.request.user.user_institute
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Institute'
        return context


class MyInstituteEditView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.UpdateView):
    model = InstitutionProfile
    context_object_name = 'my_institute'
    fields = ('institute_name', 'institute_location',
              'institute_code','gender', 'institute_pic')
    template_name = 'institution/institute/edit_my_institute.html'
    success_message = "Institute was updated successfully"
    success_url = reverse_lazy('institution:my_institute')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit My Institute'
        return context


class TransactionMethodView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = InstitutionTransactionMethod
    context_object_name = 'all_transaction_method'
    template_name = 'institution/transaction/all_transaction_method.html'

    def get_queryset(self):
        try:
            qs = InstitutionTransactionMethod.objects.filter(
                institute=self.request.user.user_institute)
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
    success_url = reverse_lazy('institution:transaction_method')

    def get_context_data(self, **kwargs):
        context = super(AddTransactionMethodView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Create Transaction Method'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        self.object.save()

        return super(AddTransactionMethodView, self).form_valid(form)


class EditTransactionMethodView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.UpdateView):
    model = InstitutionTransactionMethod
    context_object_name = 'transaction_method'
    form_class = InstitutionTransactionMethodForm
    template_name = 'institution/transaction/update_transaction_method.html'
    success_message = "Transaction Method was updated successfully"
    success_url = reverse_lazy('institution:transaction_method')

    def get_context_data(self, **kwargs):
        context = super(EditTransactionMethodView,
                        self).get_context_data(**kwargs)
        context['title'] = 'Update Transaction Method'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        self.object.save()

        return super(EditTransactionMethodView, self).form_valid(form)


class DeleteTransactionMethodView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.DeleteView):
    model = InstitutionTransactionMethod
    template_name = 'institution/transaction/delete_transaction_method.html'
    success_message = "Transaction Method was deleted successfully"
    success_url = reverse_lazy('institution:transaction_method')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Transaction Method'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteTransactionMethodView, self).delete(request, *args, **kwargs)
