from django.contrib import admin
from django.utils.html import format_html
from .models import InstitutionProfile
from django.contrib.auth import get_user_model
# Register your models here.


class InstitutionProfileAdmin(admin.ModelAdmin):
    def institute_pic_tag(self, obj):
        if obj.institute_pic:
            return format_html('<img src="{}" width="30x"/>'.format(obj.institute_pic.url))

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
