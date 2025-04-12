from django.contrib import admin

# Register your models here.

from .models import Trip, TripSchedule, TripToken
admin.site.register(Trip);
admin.site.register(TripSchedule);
admin.site.register(TripToken);
