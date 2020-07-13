from institution.models import InstitutionProfile, AdmissionSession


def on_going_admission(request):
    on_going_admission = AdmissionSession.objects.select_related(
        'institute').filter(status=True).exclude(institute__institute_pic='')
    return {'on_going_admission': on_going_admission}


def all_institute_profile(request):
    all_institute_profile = InstitutionProfile.objects.filter(
        active=True).exclude(institute_pic='')
    return {'all_institute_profile': all_institute_profile}
