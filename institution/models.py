from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from institution.tasks import set_admission_as_inactive, send_email_to_subscriber
# Create your models here.


class InstitutionProfile(models.Model):
    GENDER_CHOICES = (
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Both'),
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='user_institute')
    institute_name = models.CharField(max_length=255, default='Institute Name')
    institute_city = models.CharField(max_length=150, default='Institute City')
    institute_location = models.CharField(
        max_length=255, default='Institute Location')
    institute_code = models.CharField(max_length=50, default='Institute Code')
    application_fee = models.FloatField(default=0.0)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='3')
    institute_pic = models.ImageField(
        upload_to="institution", blank=True, null=True)
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
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField()

    class Meta:
        verbose_name = 'AdmissionSession'
        verbose_name_plural = '2. AdmissionSession'

    def save(self, *args, **kwargs):
        create_task = False
        if self.pk is None:
            create_task = True

        super(AdmissionSession, self).save(*args, **kwargs)

        if create_task and self.end_time:
            set_admission_as_inactive.apply_async(
                args=[self.id], eta=self.end_time)

    def __str__(self):
        return self.session_name


class InstituteInstruction(models.Model):
    institute = models.ForeignKey(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_instructions')
    title = models.CharField(max_length=255)
    body = RichTextField()

    class Meta:
        verbose_name = 'InstituteInstruction'
        verbose_name_plural = '3. InstituteInstruction'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    institute = models.ForeignKey(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_subscribers')
    user_email = models.EmailField()

    def __str__(self):
        return f"{self.user_email} subscribes {self.institute.institute_name}"


@receiver(post_save, sender=AdmissionSession)
def send_admission_start_msg(sender, instance, created, **kwargs):
    post_save.disconnect(send_admission_start_msg, sender=sender)

    if instance.status:
        if created:
            send_email_to_subscriber.delay(list(
                instance.institute.institute_subscribers.all().values_list('user_email', flat=True)), instance.institute.institute_name)
        else:
            send_email_to_subscriber.delay(list(
                instance.institute.institute_subscribers.all().values_list('user_email', flat=True)), instance.institute.institute_name)

    post_save.connect(send_admission_start_msg, sender=sender)


