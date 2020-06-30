from django.db import models

# Create your models here.


class ApplicantProfile(models.Model):
    GENDER_CHOICES = (
        ('0', 'Male'),
        ('1', 'Female'),
    )
    RELIGION_CHOICES = (
        ('0', 'Male'),
        ('1', 'Female'),
    )
    student_name = models.CharField(max_length=250)
    father_name = models.CharField(max_length=250)
    father_occupation = models.CharField(max_length=250)
    mother_name = models.CharField(max_length=250)
    mother_occupation = models.CharField(max_length=250)
    present_address = models.TextField()
    permanent_address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email_address = models.EmailField(max_length=254)
    birth_date = models.CharField(max_length=230)
    birth_id = models.CharField(max_length=250)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
