from django.urls import path
from . import views


app_name = "applications"

urlpatterns = [
    path('apply/<int:applicant_id>/', views.ApplyApplicationView.as_view(),
         name="apply"),

    path('application/list/', views.ApplicationListView.as_view(),
         name="application_list"),

    path('application/delete/<int:pk>/', views.DeleteApplicationView.as_view(),
         name="application_delete"),

    path('ajax/load-subjects/', views.load_subjects, name='ajax_load_subjects'),







]
