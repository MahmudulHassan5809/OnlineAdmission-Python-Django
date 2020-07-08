from django.urls import path
from . import views


app_name = "transaction"

urlpatterns = [
    path('transaction-method/',
         views.TransactionMethodView.as_view(), name="transaction_method"),
    path('transaction-method/add/',
         views.AddTransactionMethodView.as_view(), name="add_transaction_method"),
    path('transaction-method/edit/<int:pk>/',
         views.EditTransactionMethodView.as_view(), name="edit_transaction_method"),

    path('transaction-method/delete/<int:pk>/',
         views.DeleteTransactionMethodView.as_view(), name="delete_transaction_method"),

    path('application/pay-fee/<int:application_id>/<int:institute_id>/', views.PayApplicationFeeView.as_view(),
         name="pay_application_fee"),

    path('applicant/payment-list/', views.ApplicantPaymentListView.as_view(),
         name="applicant_payment_list"),

    path('institute/payment-list/', views.InstitutePaymentListView.as_view(),
         name="institute_payment_list"),

    path('institute/payment/check/<int:id>/', views.InstitutePaymentCheckView.as_view(),
         name="institute_payment_check"),


    path('applicant/transaction/details/<int:transaction_id>/',
         views.TransactionDetailsView.as_view(), name='transaction_details')
]
