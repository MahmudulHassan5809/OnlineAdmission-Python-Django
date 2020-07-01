from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin, AictiveInstitutionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AdmissionSessionForm
from django.views import View, generic
from django.contrib.auth import get_user_model
from applications.models import ApplicantPrevEducation, ApplicantProfile
from .models import InstitutionProfile, AdmissionSession
# Create your views here.


class AdmissionSessionView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = AdmissionSession
    context_object_name = 'admission_session'
    template_name = 'institution/session/adminssion_session.html'

    def get_queryset(self):
        qs = AdmissionSession.objects.filter(
            institute=self.request.user.user_institute).first()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Admission Session'
        return context


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
        # self.object.save()

        return super(CreateInstitutionSession, self).form_valid(form)


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
        # self.object.save()

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
