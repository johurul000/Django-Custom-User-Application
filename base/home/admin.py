from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'user_bio', 'profile_image')

admin.site.register(CustomUser, CustomUserAdmin)
