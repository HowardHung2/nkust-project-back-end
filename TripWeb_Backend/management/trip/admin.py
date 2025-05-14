from django.contrib import admin

# Register your models here.

from .models import Trip, TripSchedule
# admin.site.register(Trip);
# admin.site.register(TripSchedule);
# admin.site.register(TripToken);

class TripAdmin(admin.ModelAdmin):
    list_display = ("trip_code","title", "location_country") 

admin.site.register(Trip, TripAdmin)

@admin.register(TripSchedule)
class TripScheduleAdmin(admin.ModelAdmin):
    list_display = ("trip", "date", "available_spots", "price_ntd")
    list_filter = ("date","status")


