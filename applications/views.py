from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from accounts.mixins import AictiveUserRequiredMixin, AictiveApplicantRequiredMixin, AictiveInstitutionRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from applicant.models import ApplicantPrevEducation, ApplicantProfile
from institution.models import InstitutionProfile, AdmissionSession, InstitutionTransactionMethod
from .models import Application
from .forms import ApplicationForm, ApplicationPaymentForm
from django.views import View, generic
# Create your views here.


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


class ApplicationListView(AictiveApplicantRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        all_application = request.user.owner_applications.all()
        context = {
            'title': 'Application List',
            'all_application': all_application
        }

        return render(request, 'applicant/applications/applications_list.html', context)


class DeleteApplicationView(AictiveApplicantRequiredMixin, generic.edit.DeleteView):
    model = Application
    template_name = 'applicant/applications/delete_application.html'
    success_message = "Application was deleted successfully"
    success_url = reverse_lazy('applications:application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Application'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteApplicationView, self).delete(request, *args, **kwargs)


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

        return render(request, 'applicant/applications/pay_fee.html', context)
