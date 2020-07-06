from django.urls import path
from . import views


app_name = "settings"

urlpatterns = [
    path('faq/', views.SiteFaqView.as_view(),
         name="site_faq"),

]
