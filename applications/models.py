from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class ApplicantProfile(models.Model):
    GENDER_CHOICES = (
        ('1', 'Male'),
        ('2', 'Female'),
    )
    RELIGION_CHOICES = (
        ('1', 'Islam'),
        ('2', 'Hinduism'),
        ('3', 'Cristian'),
        ('4', 'Buddhist'),
    )
    FREEDOM_FIGHTER_CHOICES = (
        ('0', 'No'),
        ('1', 'Yes'),
    )
    IS_AUTISM_CHOICES = (
        ('0', 'No'),
        ('1', 'Yes'),
    )
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='user_applications')
    student_name = models.CharField(max_length=250)
    father_name = models.CharField(max_length=250)
    father_occupation = models.CharField(max_length=250)
    mother_name = models.CharField(max_length=250)
    mother_occupation = models.CharField(max_length=250)
    present_address = models.TextField()
    permanent_address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email_address = models.EmailField(max_length=254, null=True, blank=True)
    birth_date = models.CharField(max_length=230)
    birth_id = models.CharField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    religion = models.CharField(max_length=10, choices=RELIGION_CHOICES)
    blood_group = models.CharField(max_length=20)
    freedom_fighter_quota = models.CharField(
        max_length=150, choices=FREEDOM_FIGHTER_CHOICES, default="0")
    is_autism = models.CharField(
        max_length=150, choices=IS_AUTISM_CHOICES, default="0")
    height = models.FloatField(null=True, blank=True)
    local_guardian_name = models.CharField(
        max_length=250, null=True, blank=True)
    relation_with_applicant = models.CharField(
        max_length=255, null=True, blank=True)
    guardian_income = models.FloatField()
    student_pic = models.ImageField(upload_to="student")

    class Meta:
        verbose_name = 'Applicant Form'
        verbose_name_plural = '1. Applicant Form'

    def __str__(self):
        return self.student_name


class ApplicantPrevEducation(models.Model):
    BOARD_CHOICES = (
        ('1', 'Dhaka'),
        ('2', 'Khulna'),
        ('3', 'Rajshahi'),
        ('4', 'Barishal'),
        ('5', 'Jessore'),
        ('6', 'Comilla'),
    )
    EXAM_CHOICES = (
        ('1', 'SSC'),
        ('2', 'HSC')
    )
    applicant = models.ForeignKey(
        ApplicantProfile, on_delete=models.CASCADE, related_name='applicant_pre_edu')
    exam_name = models.CharField(max_length=10, choices=BOARD_CHOICES)
    board_name = models.CharField(max_length=10, choices=BOARD_CHOICES)
    institute_name = models.CharField(max_length=255)
    passing_year = models.IntegerField()
    result = models.FloatField()

    def __str__(self):
        return self.applicant.student_name
