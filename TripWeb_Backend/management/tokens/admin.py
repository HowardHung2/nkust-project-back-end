from django.contrib import admin
from .models import TripToken

# Register your models here.
@admin.register(TripToken)
class TripTokenAdmin(admin.ModelAdmin):
    list_display = ("trip_schedule", "token_amount", "status")
