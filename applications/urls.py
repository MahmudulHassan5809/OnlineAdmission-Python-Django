from django.urls import path
from . import views


app_name = "applications"

urlpatterns = [
    path('apply/<int:applicant_id>/', views.ApplicantProfileView.as_view(),
         name="apply"),
]
