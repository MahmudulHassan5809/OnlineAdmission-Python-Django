from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
# Create your models here.


class InstitutionProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='user_institute')
    institute_name = models.CharField(max_length=255)
    institute_location = models.CharField(max_length=255)
    institute_code = models.CharField(max_length=50)
    institute_pic = models.ImageField(upload_to="institution")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'InstitutionProfile'
        verbose_name_plural = '1. InstitutionProfile'

    def __str__(self):
        return f"{self.user.username} owns {self.institute_name}"


class SingleInstanceMixin(object):
    """Makes sure that no more than one instance of a given model is created."""

    def clean(self):
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ValidationError(
                "Can only create 1 %s instance Please Edit The Previous One" % model.__name__)
        super(SingleInstanceMixin, self).clean()


class AdmissionSession(SingleInstanceMixin, models.Model):
    institute = models.OneToOneField(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_session')
    session_name = models.CharField(max_length=200)
    year = models.IntegerField()
    status = models.BooleanField()

    def __str__(self):
        return self.session_name
