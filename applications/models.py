from django.db import models
import random
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from applicant.models import ApplicantProfile
from institution.models import InstitutionProfile, AdmissionSession, InstitutionSubject
# Create your models here.


def create_new_roll_number():
    return str(random.randint(1000000000, 9999999999))


class Application(models.Model):
    STATUS_CHOICES = (
        ('0', 'Pending'),
        ('1', 'Completed'),
        ('2', 'Canceled'),
        ('3', 'Waiting')
    )
    LEVEL_CHOICES = (
        ('1', 'Bachelor'),
        ('2', 'Masters'),
    )
    roll_number = models.CharField(max_length=10,
                                   editable=False,
                                   unique=True,
                                   default=create_new_roll_number())
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='owner_applications')
    applicant = models.ForeignKey(
        ApplicantProfile, on_delete=models.CASCADE, related_name='applicant_applications')
    institute = models.ForeignKey(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_applications')
    subject = models.ForeignKey(
        InstitutionSubject, on_delete=models.CASCADE, related_name='subject_applications')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='3')
    level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES)
    paid = models.BooleanField(default=False)
    admit_card = models.FileField(
        upload_to="admit_card", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = '1. Applications'

    def __str__(self):
        return f"{self.applicant.student_name} apply to {self.institute.institute_name}"
