from django.contrib import admin

from .models import Pay, Salon, Master, Service, ServiceCategory, Appointment, Address, CustomUser


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'operation_id', 'amount', 'is_success')


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'image')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image', 'category')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'salon', 'master', 'client', 'date', 'time', 'status')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'house', 'lng', 'lat')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phonenumber',)



# Register your models here.
