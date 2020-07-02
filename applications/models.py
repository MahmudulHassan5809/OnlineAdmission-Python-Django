from django.db import models
from django.contrib.auth import get_user_model
from applicant.models import ApplicantProfile
from institution.models import InstitutionProfile, AdmissionSession
# Create your models here.


class Applications(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='owner_applications')
    applicant = models.ForeignKey(
        ApplicantProfile, on_delete=models.CASCADE, related_name='applicant_applications')
    institute = models.ForeignKey(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_applications')

    def __str__(self):
        return f"{self.applicant.student_name} apply to {self.institute.institute_name}"
