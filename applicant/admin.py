from django.contrib import admin
from .models import ApplicantProfile, ApplicantPrevEducation
# Register your models here.


class ApplicantPrevEducationInline(admin.StackedInline):
    model = ApplicantPrevEducation
    extra = 0


class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ['student_name','father_name','mother_name','contact_number']
    search_fields = ['student_name','contact_number','father_name','mother_name']
    inlines = [
        ApplicantPrevEducationInline
    ]
    list_per_page = 20


admin.site.register(ApplicantProfile, ApplicantProfileAdmin)
