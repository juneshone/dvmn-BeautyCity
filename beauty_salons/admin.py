from django.contrib import admin

from .models import Pay


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'operation_id', 'amount', 'is_success')

# Register your models here.
