from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# Create your models here.


class InstitutionProfile(models.Model):
    GENDER_CHOICES = (
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Both'),
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='user_institute')
    institute_name = models.CharField(max_length=255)
    institute_location = models.CharField(max_length=255)
    institute_code = models.CharField(max_length=50)
    application_fee = models.FloatField()
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='3')
    institute_pic = models.ImageField(upload_to="institution")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'InstitutionProfile'
        verbose_name_plural = '1. InstitutionProfile'

    def __str__(self):
        return self.institute_name


class InstitutionSubject(models.Model):
    LEVEL_CHOICES = (
        ('1', 'Bachelor'),
        ('2', 'Masters'),
        ('3', 'Both'),
    )
    institute = models.ForeignKey(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_subjects')
    subject_name = models.CharField(max_length=250)
    level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject_name


# class SingleInstanceMixin(object):
#     """Makes sure that no more than one instance of a given model is created."""

#     def clean(self):
#         model = self.__class__
#         if (model.objects.count() > 0 and self.id != model.objects.get().id):
#             raise ValidationError(
#                 "Can only create 1 %s instance Please Edit The Previous One" % model.__name__)
#         super(SingleInstanceMixin, self).clean()


class AdmissionSession(models.Model):
    LEVEL_CHOICES = (
        ('1', 'Bachelor'),
        ('2', 'Masters'),
        ('3', 'Bachelor & Masters')
    )
    institute = models.OneToOneField(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_session')
    session_name = models.CharField(max_length=200)
    year = models.IntegerField()
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='3')
    status = models.BooleanField()

    class Meta:
        verbose_name = 'AdmissionSession'
        verbose_name_plural = '2. AdmissionSession'

    def __str__(self):
        return self.session_name
