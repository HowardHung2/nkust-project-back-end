# management/member/admin.py

from django.contrib import admin
from .models import UserProfile

# Define a custom admin class for UserProfile
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "xrpl_seed", "xrpl_address")  # Fields to display in the admin list view

# Register the model with the custom admin class
admin.site.register(UserProfile, UserProfileAdmin)
