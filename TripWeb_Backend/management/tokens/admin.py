from django.contrib import admin
from .models import TripToken

@admin.register(TripToken)
class TripTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token_index', 'trip_schedule', 'status', 'owner', 'order')
