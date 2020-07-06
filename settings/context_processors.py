from settings.models import SiteInfo


def site_info(request):
    site_info = SiteInfo.objects.all().first()
    return {'site_info': site_info}
