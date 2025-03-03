from django.contrib import admin
from .models import UserModel, Customer

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'phone', 'address']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'address']



admin.site.register(UserModel, UserModelAdmin)
admin.site.register(Customer,  CustomerAdmin)

