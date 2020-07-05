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

    path('pending-application/', views.PendingApplicationView.as_view(),
         name='institute_pending_application'),

    path('accepted-application/', views.AcceptedApplicationView.as_view(),
         name='institute_accepted_application'),

    path('applicant-profile/<int:applicant_id>/', views.ApplicantProfileView.as_view(),
         name='applicant_profile'),

    path('applicant-admit-card/<int:application_id>/', views.ApplicantAdmitCardView.as_view(),
         name='admit_card_generate'),
]
