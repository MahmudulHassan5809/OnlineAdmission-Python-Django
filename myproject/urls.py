from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import HomeLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('applicant/', include('applicant.urls', namespace='applicant')),
    path('institution/', include('institution.urls', namespace='institution')),
    path('applications/', include('applications.urls', namespace='applications')),
    path('transaction/', include('transaction.urls', namespace='transaction')),
    path('settings/', include('settings.urls', namespace='settings')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', HomeLoginView.as_view(), name="home_login"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.FORCE_STATIC_FILE_SERVING and not settings.DEBUG:
    settings.DEBUG = True
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    settings.DEBUG = False


admin.site.site_header = "VortiBD Admin"
admin.site.site_title = "VortiBD Admin Portal"
admin.site.index_title = "VortiBD to Finder Researcher Portal"
