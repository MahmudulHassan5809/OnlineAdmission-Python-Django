from celery.decorators import task
from django.shortcuts import get_object_or_404


@task()
def set_admission_as_inactive(session_id):
    from instituion.models import AdmissionSession
    session_object = get_object_or_404(AdmissionSession, id=session_id)
    session_object.status = False
    session_object.save()
