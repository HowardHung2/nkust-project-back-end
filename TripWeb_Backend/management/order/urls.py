from django.urls import path
from . import views

urlpatterns = [
    path("order/<uuid:schedule_id>/purchase/", views.purchase_trip, name='purchase_trip'),
    path("my_order/", views.TripScheduleByUserListView.as_view(), name='my_order'),
]
