from django.contrib import admin
from .models import ApplicationInstruction, ApplicationInstructionList, SiteInfo, SiteFaq
# Register your models here.


class ApplicationInstructionListInline(admin.StackedInline):
    model = ApplicationInstructionList
    extra = 0


class ApplicationInstructionAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ('title',)
    list_per_page = 20
    inlines = [
        ApplicationInstructionListInline
    ]


admin.site.register(ApplicationInstruction, ApplicationInstructionAdmin)


class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_phone', 'site_email']

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


admin.site.register(SiteInfo, SiteInfoAdmin)


class SiteFaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']
    list_per_page = 20


admin.site.register(SiteFaq, SiteFaqAdmin)
