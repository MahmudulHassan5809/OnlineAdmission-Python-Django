from celery.decorators import task
from django.shortcuts import get_object_or_404
from celery import shared_task
from django.core.mail import send_mass_mail


@task()
def set_admission_as_inactive(session_id):
    from instituion.models import AdmissionSession
    session_object = get_object_or_404(AdmissionSession, id=session_id)
    session_object.status = False
    session_object.save()


@shared_task
def send_email_to_subscriber(institute_subscribers, institute_name):
    subject = 'Admission Session Is Now Active'
    message = f'Message From {institute_name}.Our Admission is Open Now.Please Get Form If You Are Interested'
    mail_tuple = (subject, message, 'no_responder@vortibd.com',
                  institute_subscribers)
    send_mass_mail((mail_tuple,))
