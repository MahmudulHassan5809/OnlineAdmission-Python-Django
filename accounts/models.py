from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'


# Create your models here.


class Profile(models.Model):
    USER_CHOICES = (
        ('0', 'Admission Holder'),
        ('1', 'Institute Holder'),
    )

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)

    profile_pic = models.ImageField(
        upload_to="profile", default="profile/default.png")

    user_type = models.CharField(
        max_length=10, choices=USER_CHOICES)

    active = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = '2. Profile'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    from institution.models import InstitutionProfile
    try:
        if created:
            Profile.objects.create(user=instance)
            if instance.user_profile.user_type == '1' and not InstitutionProfile.objects.filter(user=instance).first():
                InstitutionProfile.objects.create(user=instance)
        else:
            if instance.user_profile.user_type == '1' and not InstitutionProfile.objects.filter(user=instance).first():
                InstitutionProfile.objects.create(user=instance)
            instance.user_profile.save()
    except Exception as e:
        pass
