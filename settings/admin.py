from django.contrib import admin
from .models import ApplicationInstruction, ApplicationInstructionList
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
