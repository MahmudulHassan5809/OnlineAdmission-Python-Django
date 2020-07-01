from django.db import models
from django.contrib.auth import get_user_model
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
