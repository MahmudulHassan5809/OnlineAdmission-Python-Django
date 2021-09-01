from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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

from institution.models import InstitutionProfile, AdmissionSession, InstitutionSubject, InstituteInstruction


from institution.forms import AdmissionSessionForm, InstitutionSubjectForm, InstituteSearchForm, InstituteInstructionForm, SubscriptionForm

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
            qs = AdmissionSession.objects.select_related('institute').filter(
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
            qs = AdmissionSession.objects.select_related('institute').filter(
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
    fields = ('institute_name', 'application_fee', 'institute_city', 'institute_location',
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
        qs = InstitutionSubject.objects.select_related('institute').filter(
            institute=self.request.user.user_institute).only("institute__institute_name", "subject_name", "level")
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
        qs = Application.objects.select_related('owner', 'applicant', 'institute', 'subject').filter(
            institute=self.request.user.user_institute, status='0').only("owner__username", "applicant__student_name", "roll_number", "institute__institute_name", "subject__subject_name", "level", "paid", "created_at")
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
        qs = Application.objects.select_related('owner__user_profile', 'applicant', 'institute', 'subject').filter(
            institute=self.request.user.user_institute, status='1').only("owner__username","owner__user_profile__phone_number", "applicant__student_name", "roll_number", "institute__institute_name", "subject__subject_name", "level", "paid", "created_at")
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


@method_decorator(csrf_exempt, name='dispatch')
class InstituteSearchView(generic.ListView):
    model = InstitutionProfile
    context_object_name = 'institute_list'
    paginate_by = 10
    template_name = 'common/search_results.html'

    def get_queryset(self):
        if self.request.GET.get('city'):
            subject_id = self.request.GET.get('subject')
            try:
                subject_obj = get_object_or_404(
                    InstitutionSubject, id=subject_id)
                institute_list = subject_obj.institute_subjects.all()
            except Exception as e:
                institute_list = InstitutionProfile.objects.filter(active=True)
        else:
            institute_list = InstitutionProfile.objects.filter(active=True)

        if self.request.GET.get('city'):
            city = self.request.GET.get('city')
            institute_list = institute_list.filter(institute_city__exact=city)
        return institute_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('slug')
        context['institute_search_form'] = InstituteSearchForm()
        context['title'] = f'Search Results'
        return context


class InstituteInstructionView(AictiveInstitutionRequiredMixin, generic.ListView):
    model = InstituteInstruction
    context_object_name = 'instruction_list'
    template_name = 'institution/instruction/instruction_list.html'

    def get_queryset(self):
        qs = InstituteInstruction.objects.select_related('institute').filter(
            institute=self.request.user.user_institute).only("institute__institute_name","title","body")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Institute Instruction'
        return context


class CreateInstructionView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.CreateView):
    model = InstituteInstruction
    form_class = InstituteInstructionForm
    template_name = 'institution/instruction/create_instruction.html'
    success_message = "Instruction  was created successfully"
    success_url = reverse_lazy('institution:institute_instruction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Instruction'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        # self.object.save()

        return super(CreateInstructionView, self).form_valid(form)


class EditInstructionView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.UpdateView):
    model = InstituteInstruction
    form_class = InstituteInstructionForm
    context_object_name = 'instruction_obj'
    template_name = 'institution/instruction/update_instruction.html'
    success_message = "Instruction  was updated successfully"
    success_url = reverse_lazy('institution:institute_instruction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Instruction'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.institute = self.request.user.user_institute
        return super(EditInstructionView, self).form_valid(form)


class DeleteInstructionView(SuccessMessageMixin, AictiveInstitutionRequiredMixin, generic.edit.DeleteView):
    model = InstituteInstruction
    template_name = 'institution/instruction/delete_instruction.html'
    success_message = "Instruction was deleted successfully"
    success_url = reverse_lazy('institution:institute_instruction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Instruction'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteInstructionView, self).delete(request, *args, **kwargs)


class InstituteInstructionDetailsView(View):
    def get(self, request, *args, **kwargs):
        institution_id = kwargs.get('institution_id')
        institution_obj = get_object_or_404(
            InstitutionProfile, id=institution_id)
        institution_instructions = institution_obj.institute_instructions.all()

        subscription_form = SubscriptionForm()

        context = {
            'title': f"{institution_obj.institute_name}'s Instruction",
            'institution_obj': institution_obj,
            'institution_instructions': institution_instructions,
            'subscription_form': subscription_form
        }

        return render(request, 'common/institute_instruction.html', context)


class InstituteSubscribeView(View):
    def post(self, request, *args, **kwargs):
        institution_id = kwargs.get('institution_id')
        subscription_form = SubscriptionForm(request.POST)

        if subscription_form.is_valid():
            institution_obj = get_object_or_404(
                InstitutionProfile, id=institution_id)
            save_obj = subscription_form.save(commit=False)
            save_obj.institute = institution_obj
            save_obj.save()
            messages.success(request, 'Thanks For Subscribing Us')
            return redirect('institution:institute_instruction_details', institution_id)
        else:
            messages.error(request, 'Something Went Wrong Try Again')
            return redirect('institution:institute_instruction_details', institution_id)
