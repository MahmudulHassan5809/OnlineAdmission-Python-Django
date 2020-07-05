from django.db import models
from django.contrib.auth import get_user_model
from applicant.models import ApplicantProfile
from institution.models import InstitutionProfile, AdmissionSession, InstitutionSubject
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
    admit_card = models.FileField(
        upload_to="admit_card", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.applicant.student_name} apply to {self.institute.institute_name}"
