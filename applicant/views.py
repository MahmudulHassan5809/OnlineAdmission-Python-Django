from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db import transaction
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ApplicantPrevEducationFormSet, ApplicantProfileForm
from django.contrib.auth import get_user_model
from .models import ApplicantPrevEducation, ApplicantProfile
from django.views import View, generic
# Create your views here.


class ApplicantProfileView(generic.ListView):
    model = ApplicantProfile
    context_object_name = 'all_applicant_profile'
    template_name = 'applicant/applicant/all_applicant_profile.html'

    def get_queryset(self):
        qs = ApplicantProfile.objects.filter(owner=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Applicant Profile'
        return context


class CreateApplicantProfileView(SuccessMessageMixin, AictiveApplicantRequiredMixin, generic.CreateView):
    model = ApplicantProfile
    form_class = ApplicantProfileForm
    template_name = 'applicant/applicant/create_applicant_profile.html'
    success_message = "Applicant Profile was created successfully"
    success_url = reverse_lazy('applicant:applicant_profile')

    def get_context_data(self, **kwargs):
        context = super(CreateApplicantProfileView,
                        self).get_context_data(**kwargs)
        if self.request.POST:
            context['preveducation'] = ApplicantPrevEducationFormSet(
                self.request.POST, self.request.FILES)
        else:
            context['preveducation'] = ApplicantPrevEducationFormSet()
        context['title'] = 'Create Applicant Profile'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        preveducation = context['preveducation']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()

        if preveducation.is_valid():
            preveducation.instance = self.object
            preveducation.save()
        return super(CreateApplicantProfileView, self).form_valid(form)


class EditApplicantProfileView(SuccessMessageMixin, AictiveApplicantRequiredMixin, generic.UpdateView):
    model = ApplicantProfile
    context_object_name = 'applicant_profile'
    form_class = ApplicantProfileForm
    success_message = "Applicant Profile was updated successfully"
    template_name = 'applicant/applicant/update_applicant_profile.html'
    success_url = reverse_lazy('applicant:applicant_profile')

    def get_context_data(self, **kwargs):
        context = super(EditApplicantProfileView,
                        self).get_context_data(**kwargs)
        if self.request.POST:
            context['preveducation'] = ApplicantPrevEducationFormSet(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            query_set = ApplicantPrevEducation.objects.filter(
                applicant=self.object)
            print(query_set)
            context['preveducation'] = ApplicantPrevEducationFormSet(
                instance=self.object)

        context['title'] = 'Update Applicant Profile'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        preveducation = context['preveducation']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            self.object.save()

        if preveducation.is_valid():
            preveducation.instance = self.object
            preveducation.save()
        return super(EditApplicantProfileView, self).form_valid(form)


class DeleteApplicantProfileView(SuccessMessageMixin, AictiveApplicantRequiredMixin, generic.edit.DeleteView):
    model = ApplicantProfile
    template_name = 'applicant/applicant/delete_applicant_profile.html'
    success_message = "Applicant Profile was deleted successfully"
    success_url = reverse_lazy('applicant:applicant_profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Profile'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteApplicantProfileView, self).delete(request, *args, **kwargs)
