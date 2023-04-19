from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']
    list_display = ['username', 'email', 'is_staff']
    list_filter = ['username', 'email', 'is_staff', 'date_joined']


admin.site.register(User, UserAdmin)
