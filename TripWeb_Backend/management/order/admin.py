from django.contrib import admin

from .models import TripOrder

@admin.register(TripOrder)
class TripOrderAdmin(admin.ModelAdmin):
    list_display = ("trip_schedule", "user", "spots_booked", "booking_date")