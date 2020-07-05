from django.contrib import admin
from .models import InstitutionTransactionMethod, ApplicationPayment
# Register your models here.


class InstitutionTransactionMethodAdmin(admin.ModelAdmin):
    list_display = ['institute', 'method_name', 'account_number']
    search_fields = ['institute__institute_name',
                     'method_name', 'account_number']
    list_filter = ['institute__institute_name', ]
    list_per_page = 20


admin.site.register(InstitutionTransactionMethod,
                    InstitutionTransactionMethodAdmin)


class ApplicationPaymentAdmin(admin.ModelAdmin):
    list_display = ['application', 'owner', 'institute', 'payment_method', 'send_from',
                    'transaction_number', 'status', 'completed', 'pending', 'cancel', 'created_at']
    search_fields = ['owner__username', 'institute__institute_name',
                     'send_from', 'payment_method__method_name']
    list_filter = ['status', 'completed', 'pending', 'cancel']
    list_editable = ['status', 'completed', 'pending', 'cancel']
    list_per_page = 20


admin.site.register(ApplicationPayment,
                    ApplicationPaymentAdmin)
