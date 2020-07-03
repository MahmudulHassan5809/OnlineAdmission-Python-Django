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

    path('institute/view/',
         views.MyInstituteView.as_view(), name="my_institute"),
    path('institute/edit/<int:pk>/',
         views.MyInstituteEditView.as_view(), name="my_institute_edit"),

    path('institute/subject/',
         views.MyInstituteSubjectView.as_view(), name="my_institute_subject"),

    path('institute/subject/add/',
         views.AddMyInstituteSubjectView.as_view(), name="my_institute_subject_add"),
    path('institute/subject/edit/<int:pk>/',
         views.EditMyInstituteSubjectView.as_view(), name="my_institute_subject_edit"),
    path('institute/subject/delete/<int:pk>/',
         views.DeleteMyInstituteSubjectView.as_view(), name="my_institute_subject_delete"),


    path('transaction-method/',
         views.TransactionMethodView.as_view(), name="transaction_method"),
    path('transaction-method/add/',
         views.AddTransactionMethodView.as_view(), name="add_transaction_method"),
    path('transaction-method/edit/<int:pk>/',
         views.EditTransactionMethodView.as_view(), name="edit_transaction_method"),
    path('transaction-method/delete/<int:pk>/',
         views.DeleteTransactionMethodView.as_view(), name="delete_transaction_method"),
]
