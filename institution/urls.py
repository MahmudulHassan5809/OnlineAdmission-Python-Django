from django.urls import path
from . import views


app_name = "institution"

urlpatterns = [
    path('admission-session/',
         views.AdmissionSessionView.as_view(), name="admission_session"),
    path('admission-session/create/',
         views.CreateInstitutionSession.as_view(), name="create_session"),
    path('admission-session/delete/<int:pk>/',
         views.DeleteInstitutionSession.as_view(), name="delete_session"),
    path('admission-session/edit/<int:pk>/',
         views.UpdateInstitutionSession.as_view(), name="update_session"),
]
