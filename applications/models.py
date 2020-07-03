from django.db import models
from django.contrib.auth import get_user_model
from applicant.models import ApplicantProfile
from institution.models import InstitutionProfile, AdmissionSession, InstitutionTransactionMethod, InstitutionSubject
# Create your models here.


class Application(models.Model):
    STATUS_CHOICES = (
        ('0', 'Pending'),
        ('1', 'Completed'),
        ('2', 'Canceled')
    )
    LEVEL_CHOICES = (
        ('1', 'Bachelor'),
        ('2', 'Masters'),
    )
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='owner_applications')
    applicant = models.ForeignKey(
        ApplicantProfile, on_delete=models.CASCADE, related_name='applicant_applications')
    institute = models.ForeignKey(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_applications')
    subject = models.ForeignKey(
        InstitutionSubject, on_delete=models.CASCADE, related_name='subject_applications')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='0')
    level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.applicant.student_name} apply to {self.institute.institute_name}"


class ApplicationPayment(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(
        InstitutionTransactionMethod, on_delete=models.CASCADE)
    send_from = models.CharField(max_length=20)
    transaction_number = models.CharField(max_length=50)

    def __str__(self):
        return self.payment_method.method_name
