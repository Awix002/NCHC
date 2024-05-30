from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'province_state_name', 'city', 'address', 'date_of_birth', 'gender')
    # Add any other configurations as needed

admin.site.register(UserProfile, UserProfileAdmin)
