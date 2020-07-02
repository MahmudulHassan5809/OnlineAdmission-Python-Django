from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin, AictiveInstitutionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from applicant.models import ApplicantPrevEducation, ApplicantProfile
from institution.models import InstitutionProfile, AdmissionSession, InstitutionTransactionMethod
from django.views import View, generic
# Create your views here.


class ApplicantProfileView(AictiveApplicantRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        applicant_id = kwargs.get('applicant_id')
        all_institute = InstitutionProfile.objects.filter(
            active=True).values('institute_name', 'id')

        context = {
            'title': 'Apply',
            'applicant_id': applicant_id,
            'all_institute': all_institute
        }

        return render(request, 'applicant/applications/apply.html', context)
