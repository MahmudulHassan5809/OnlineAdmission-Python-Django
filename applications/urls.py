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

    path('application/pay-fee/<int:application_id>/<int:institute_id>/', views.PayApplicationFeeView.as_view(),
         name="pay_application_fee"),
]
