from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.db import transaction
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin
from django.contrib import messages
from django.core import serializers
import json
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.models import Application
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
        qs = ApplicantProfile.objects.select_related(
            'owner').filter(owner=self.request.user).only("owner__username", "father_name", "mother_name", "student_name", "student_pic")
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
            if preveducation.is_valid():
                self.object = form.save(commit=False)
                self.object.owner = self.request.user
                self.object.save()
                preveducation.instance = self.object
                preveducation.save()
                return redirect('applicant:applicant_profile')
            else:
                return self.render_to_response(self.get_context_data(form=form))

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
            query_set = ApplicantPrevEducation.objects.select_related('applicant').filter(
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
            if preveducation.is_valid():
                form.save()
                preveducation.instance = self.object
                preveducation.save()
                return redirect('applicant:applicant_profile')
            else:
                return self.render_to_response(self.get_context_data(form=form))


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


class ApplicationStatusView(AictiveApplicantRequiredMixin, generic.edit.DeleteView):
    def get(self, request, *args, **kwargs):
        applicant_id = kwargs.get('applicant_id')
        applicant_obj = get_object_or_404(ApplicantProfile, id=applicant_id)
        application_obj = list(
            Application.objects.filter(applicant=applicant_obj))

        data = serializers.serialize('json', application_obj)
        return HttpResponse(data, content_type='application/json')


class ApplicantAdmitCardView(AictiveApplicantRequiredMixin, generic.ListView):
    model = Application
    context_object_name = 'applicant_admit_card'
    template_name = 'applicant/admit_card/admit_card.html'
    paginate_by = 10

    def get_queryset(self):
        qs = Application.objects.select_related('owner', 'applicant', 'institute', 'subject').filter(
            owner=self.request.user, status='1', paid=True).only("applicant__student_name","institute__institute_name","subject__subject_name","level","admit_card","owner__username")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Admit Card'
        return context

    # def get(self, request, *args, **kwargs):
    #     applicant_admit_card = Application.objects.filter(
    #         owner=request.user, status='1', paid=True)
    #     context = {
    #         'title': 'Admit Card',
    #         'applicant_admit_card': applicant_admit_card
    #     }

    #     return render(request, 'applicant/admit_card/admit_card.html', context)
