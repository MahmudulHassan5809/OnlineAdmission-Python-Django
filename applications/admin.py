from django.contrib import admin
from .models import Application
# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['owner', 'applicant', 'institute', 'subject',
                    'status', 'level', 'paid', 'admit_card', 'created_at']

    search_fields = ['owner__username', 'applicant__student_name',
                     'institute__institute_name', 'subject__subject_name']
    list_filter = ['paid', 'level','status']
    list_editable = ['paid', 'level','status']
    list_per_page = 20


admin.site.register(Application, ApplicationAdmin)
