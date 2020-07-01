from django.urls import path
from . import views


app_name = "applications"

urlpatterns = [
    path('profile/', views.ApplicantProfileView.as_view(),
         name="applicant_profile"),
    path('create/profile/', views.CreateApplicantProfileView.as_view(),
         name="create_applicant_profile"),
    path('edit/profile/<int:pk>/', views.EditApplicantProfileView.as_view(),
         name="edit_applicant_profile"),
    path('delete/profile/<int:pk>/', views.DeleteApplicantProfileView.as_view(),
         name="delete_applicant_profile"),
]
