from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

app_name = "accounts"
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login_success/', views.LoginSuccess.as_view(), name='login_success'),
    path('my-profile/', views.MyProfileView.as_view(), name="my_profile"),
    path('change-password/', views.ChangePasswordView.as_view(),
         name="change_password"),
    path('logout/', auth_views.LogoutView.as_view(template_name='common/logout.html',
                                                  extra_context={
                                                      'title': 'Logout',
                                                  }), name="logout"),


    path('applicant/dashboard/',
         views.ApplicantDashboardView.as_view(), name="applicant_dashboard"),
    path('institution/dashboard/',
         views.InstitutionDashboardView.as_view(), name="institution_dashboard"),

    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]
