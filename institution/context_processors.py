from institution.models import InstitutionProfile, AdmissionSession


def on_going_admission(request):
    on_going_admission = AdmissionSession.objects.select_related(
        'institute').filter(status=True)
    return {'on_going_admission': on_going_admission}