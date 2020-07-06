from django.contrib import admin
from django.utils.html import format_html
from .models import InstitutionProfile, InstitutionSubject, AdmissionSession, InstituteInstruction
from django.contrib.auth import get_user_model
# Register your models here.


class InstitutionSubjectInline(admin.StackedInline):
    model = InstitutionSubject
    extra = 0


class InstitutionProfileAdmin(admin.ModelAdmin):
    def institute_pic_tag(self, obj):
        if obj.institute_pic:
            return format_html('<img src="{}" width="30x"/>'.format(obj.institute_pic.url))

    inlines = [InstitutionSubjectInline]
    institute_pic_tag.short_description = 'Instituion Image'

    list_display = ["institute_name", "institute_location",
                    "institute_code", "institute_pic_tag", "owner_name", "owner_email", "active"]

    search_fields = ('user__username', 'institute_name', 'user__email',)
    list_filter = ['active']
    list_editable = ['active']
    #autocomplete_fields = ['user']
    list_per_page = 20

    def owner_name(self, obj):
        return obj.user.username

    def owner_email(self, obj):
        return obj.user.email

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = get_user_model().objects.filter(
                user_profile__user_type='1')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(InstitutionProfile, InstitutionProfileAdmin)


class AdmissionSessionAdmin(admin.ModelAdmin):
    list_display = ['institute', 'session_name', 'year', 'level', 'status']
    search_fields = ['institute__institute_name', 'session_name']
    list_filter = ['level', 'status']
    list_editable = ['status']
    list_per_page = 20


admin.site.register(AdmissionSession, AdmissionSessionAdmin)


class InstituteInstructionAdmin(admin.ModelAdmin):
    list_display = ['institute', 'title']
    search_fields = ['institute__institute_name', 'body', 'title']
    list_filter = ['institute__institute_name']
    list_per_page = 20


admin.site.register(InstituteInstruction, InstituteInstructionAdmin)
