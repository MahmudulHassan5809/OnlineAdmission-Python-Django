from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db import transaction
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ApplicantPrevEducationFormSet, ApplicantProfileForm
from django.contrib.auth import get_user_model
from .models import ApplicantPrevEducation, ApplicantProfile
from django.views import View, generic
# Create your views here.


class ApplicantProfileView(generic.ListView):
    model = ApplicantProfile
    context_object_name = 'all_applicant_profile'
    template_name = 'applicant/applications/all_applicant_profile.html'

    def get_queryset(self):
        qs = ApplicantProfile.objects.filter(owner=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Applicant Profile'
        return context


class CreateApplicantProfileView(AictiveApplicantRequiredMixin, generic.CreateView):
    model = ApplicantProfile
    form_class = ApplicantProfileForm
    template_name = 'applicant/applications/create_applicant_profile.html'
    success_url = reverse_lazy('applications:applicant_profile')

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


class EditApplicantProfileView(AictiveApplicantRequiredMixin, View):
    pass
