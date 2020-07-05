from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core import serializers
import json
from django.urls import reverse_lazy
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin, AictiveInstitutionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .render import Render
from django.core.files import File
from io import BytesIO
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
    fields = ('institute_name', 'application_fee', 'institute_location',
              'institute_code', 'gender', 'institute_pic')
    template_name = 'institution/institute/edit_my_institute.html'
    success_message = "Institute was updated successfully"
    success_url = reverse_lazy('institution:my_institute')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit My Institute'
        return context


class MyInstituteSubjectView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = InstitutionSubject
    paginate_by = 10
    context_object_name = 'all_subject'
    template_name = 'institution/subjects/all_subject.html'

    def get_queryset(self):
        qs = InstitutionSubject.objects.filter(
            institute=self.request.user.user_institute)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Institute Subjects'
        return context


class AddMyInstituteSubjectView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.CreateView):
    model = InstitutionSubject
    form_class = InstitutionSubjectForm
    template_name = 'institution/subjects/add_subject.html'
    success_message = "Subject  was added successfully"
    success_url = reverse_lazy('institution:my_institute_subject')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Subject'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        self.object.save()

        return super(AddMyInstituteSubjectView, self).form_valid(form)


class EditMyInstituteSubjectView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.UpdateView):
    model = InstitutionSubject
    context_object_name = 'subject'
    form_class = InstitutionSubjectForm
    template_name = 'institution/subjects/update_subject.html'
    success_message = "Subject  was updated successfully"
    success_url = reverse_lazy('institution:my_institute_subject')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Subject'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        self.object.save()

        return super(EditMyInstituteSubjectView, self).form_valid(form)


class DeleteMyInstituteSubjectView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.DeleteView):
    model = InstitutionSubject
    template_name = 'institution/subjects/delete_subject.html'
    success_message = "Subject was deleted successfully"
    success_url = reverse_lazy('institution:my_institute_subject')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Subject'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteMyInstituteSubjectView, self).delete(request, *args, **kwargs)


class PendingApplicationView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = Application
    paginate_by = 10
    context_object_name = 'pending_applications'
    template_name = 'institution/applications/pending_applications.html'

    def get_queryset(self):
        qs = Application.objects.filter(
            institute=self.request.user.user_institute, status='0')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pending Application'
        return context


class AcceptedApplicationView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = Application
    paginate_by = 10
    context_object_name = 'accepted_applications'
    template_name = 'institution/applications/accepted_applications.html'

    def get_queryset(self):
        qs = Application.objects.filter(
            institute=self.request.user.user_institute, status='1')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Accepted Application'
        return context


class ApplicantProfileView(AictiveInstitutionRequiredMixin, View):
    def get(self, requestm, *args, **kwargs):
        applicant_id = kwargs.get('applicant_id')
        applicant_obj = get_object_or_404(ApplicantProfile, pk=applicant_id)

        all_objects = list(ApplicantProfile.objects.filter(id=applicant_id)
                           ) + list(ApplicantPrevEducation.objects.filter(applicant=applicant_obj))

        data = serializers.serialize('json', all_objects)

        return HttpResponse(data, content_type='application/json')


class ApplicantAdmitCardView(AictiveInstitutionRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        application_id = kwargs.get('application_id')
        application_obj = get_object_or_404(Application, id=application_id)
        applicant_obj = application_obj.applicant
        institute_obj = application_obj.institute

        context = {
            'application_obj': application_obj,
            'applicant_obj': applicant_obj,
            'institute_obj': institute_obj
        }
        admit_card = Render.render(
            'institution/admit_card/admit_card.html', context)

        filename = f"{applicant_obj.student_name}-admitcard.pdf"

        application_obj.admit_card.save(
            filename, File(BytesIO(admit_card.content)))

        return admit_card
