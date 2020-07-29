from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin, AictiveInstitutionRequiredMixin
from django.contrib import messages
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


def load_subjects(request):
    institute_id = request.GET.get('institute')
    subjects = InstitutionSubject.objects.filter(
        institute_id=institute_id, active=True)
    return render(request, 'applicant/applications/subject_dropdown_list_options.html', {'subjects': subjects})


class ApplyApplicationView(AictiveApplicantRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        applicant_id = kwargs.get('applicant_id')
        applicant_obj = get_object_or_404(
            ApplicantProfile, id=applicant_id)
        application_form = ApplicationForm()

        context = {
            'title': 'Apply',
            'applicant_id': applicant_id,
            'application_form': application_form
        }

        return render(request, 'applicant/applications/apply.html', context)

    def post(self, request, *args, **kwargs):
        applicant_id = kwargs.get('applicant_id')
        application_form = ApplicationForm(request.POST)

        if application_form.is_valid():
            institute_id = request.POST.get('institute')
            institute_obj = get_object_or_404(
                InstitutionProfile, id=institute_id)
            applicant_obj = get_object_or_404(
                ApplicantProfile, id=applicant_id)

            if institute_obj.gender == '1' and applicant_obj.gender == '2':
                messages.error(request, f"{institute_obj.institute_name} Is Only Allow Male Student")
                return redirect('applications:apply', applicant_obj.id)
            if institute_obj.gender == '2' and applicant_obj.gender == '1':
                messages.error(request, f"{institute_obj.institute_name} Is Only Allow Female Student")
                return redirect('applications:apply', applicant_obj.id)

            check_application = Application.objects.filter(
                applicant=applicant_obj, institute=institute_obj).first()

            if check_application and check_application.paid:
                messages.info(request,
                              f"You Already Apply For {institute_obj.institute_name}.Please Wiat For Admit Card")
                return redirect('applications:application_list')
            if check_application and not check_application.paid:
                messages.info(request,
                              f"You Already Apply For {institute_obj.institute_name}.Please Pay The Fees")
                return redirect('applications:application_list')

            check_session = AdmissionSession.objects.filter(
                institute=institute_obj, status=True).first()

            if not check_session:
                messages.error(request, f"Now Admission Is Closed For {institute_obj.institute_name}")
                return redirect('applications:apply', applicant_obj.id)

            if check_session.level == '1' and request.POST.get('level') == '2':
                messages.error(request, f"{institute_obj.institute_name} Only Avialable For Bachelor Admission")
                return redirect('applications:apply', applicant_obj.id)

            if check_session.level == '2' and request.POST.get('level') == '1':
                messages.error(request, f"{institute_obj.institute_name} Only Avialable For Masters Admission")
                return redirect('applications:apply', applicant_obj.id)

            subject_obj = get_object_or_404(
                InstitutionSubject, id=request.POST.get('subject'))

            if subject_obj.level == '1' and request.POST.get('level') == '2':
                messages.error(request, f"{subject_obj.subject_name} In {institute_obj.institute_name} Only Avialable For Bachelor")
                return redirect('applications:apply', applicant_obj.id)

            if subject_obj.level == '2' and request.POST.get('level') == '1':
                messages.error(request, f"{subject_obj.subject_name} In {institute_obj.institute_name} Only Avialable For Masters")
                return redirect('applications:apply', applicant_obj.id)

            application_form_obj = application_form.save(commit=False)
            application_form_obj.owner = request.user
            application_form_obj.applicant = applicant_obj
            application_form_obj.save()
            messages.success(request, f"Apply For {applicant_obj.student_name} In {institute_obj.institute_name} Is Successfully Completed")
            return redirect('applications:application_list')
        else:
            context = {
                'title': 'Apply',
                'applicant_id': applicant_id,
                'application_form': application_form
            }
            return render(request, 'applicant/applications/apply.html', context)


class ApplicationListView(AictiveApplicantRequiredMixin, generic.ListView):
    model = Application
    template_name = 'applicant/applications/applications_list.html'
    context_object_name = 'all_application'
    paginate_by = 10

    def get_queryset(self):
        qs = self.request.user.owner_applications.select_related("owner","applicant","institute","subject").only("owner__username","applicant__student_name","institute__institute_name","level","status","paid","subject__subject_name").all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Application List'
        return context

    # def get(self, request, *args, **kwargs):
    #     all_application = request.user.owner_applications.all()
    #     context = {
    #         'title': 'Application List',
    #         'all_application': all_application
    #     }

    #     return render(request, 'applicant/applications/applications_list.html', context)


class DeleteApplicationView(AictiveApplicantRequiredMixin, generic.edit.DeleteView):
    model = Application
    template_name = 'applicant/applications/delete_application.html'
    success_message = "Application was deleted successfully"
    success_url = reverse_lazy('applications:application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Application'
        return context

    def render_to_response(self, context):
        if self.object.status == '1':
            messages.info(
                self.request, 'Sorry You Can Not Delete Application After Completed')
            return redirect('applications:application_list')
        return super().render_to_response(context)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteApplicationView, self).delete(request, *args, **kwargs)
