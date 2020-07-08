from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from applications.models import Application
from institution.models import InstitutionProfile, AdmissionSession, InstitutionSubject
# Create your models here.


class InstitutionTransactionMethod(models.Model):
    institute = models.ForeignKey(
        InstitutionProfile, on_delete=models.CASCADE, related_name='institute_transaction')
    method_name = models.CharField(max_length=50)
    reference_id = models.CharField(max_length=50)
    counter_no = models.IntegerField()
    account_number = models.CharField(max_length=50)
    instruction = models.TextField()

    class Meta:
        verbose_name = 'Institution Transaction'
        verbose_name_plural = '1. Institution Transaction'

    def __str__(self):
        return f"{self.method_name} -- {self.account_number}"


class ApplicationPayment(models.Model):
    STATUS_CHOICES = (
        ('0', 'Pending'),
        ('1', 'Completed'),
        ('2', 'Canceled')
    )
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    institute = models.ForeignKey(
        InstitutionProfile, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(
        InstitutionTransactionMethod, on_delete=models.CASCADE)
    send_from = models.CharField(max_length=20)
    transaction_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='0')
    completed = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    cancel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = 'ApplicationPayment'
        verbose_name_plural = '2. ApplicationPayment'

    def __str__(self):
        return self.payment_method.method_name


# Payment
@receiver(post_save, sender=ApplicationPayment)
def applicant_payment(sender, instance, created, **kwargs):
    if not instance.completed:
        if created and instance.application.status == '3':
            instance.application.status = '0'
            instance.application.save()
        if instance.status == "0" and not instance.pending:
            instance.pending = True
            instance.application.status = '0'
            instance.save()
            instance.application.save()
        if instance.status == "2" and not instance.cancel:
            instance.cancel = True
            instance.completed = True
            instance.application.status = '2'
            instance.save()
            instance.application.save()
        if instance.status == '1':
            instance.completed = True
            instance.application.status = '1'
            instance.application.paid = True
            instance.save()
            instance.application.save()
