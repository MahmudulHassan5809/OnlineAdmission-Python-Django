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

    path('application/pay-fee/<int:application_id>/<int:institute_id>/', views.PayApplicationFeeView.as_view(),
         name="pay_application_fee"),

    path('applicant/payment-list/', views.ApplicantPaymentListView.as_view(),
         name="applicant_payment_list"),

    path('institute/payment-list/', views.InstitutePaymentListView.as_view(),
         name="institute_payment_list"),

    path('institute/payment/check/<int:id>/', views.InstitutePaymentCheckView.as_view(),
         name="institute_payment_check"),

]
