from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# router = DefaultRouter()
# router.register(r'trip', views.TripViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("trips/", views.TripListView.as_view(), name="trip"),
    path("trips/<uuid:pk>/", views.TripDetailView.as_view(), name="trip_detail"),
    path("schedule/", views.TripScheduleListView.as_view(), name="trip_schedule_list"),
    path("schedule/<uuid:pk>/", views.TripSchedule, name="trip_schedule_detail"),




    # path("api/get_trips/", views.get_trips, name='get_trip'),
    # path('api/get_trips_schedule/', views.get_trips_api_schedule.as_view(), name='tour_data'),
    # path("mytrips/", views.TripScheduleByUserListView.as_view(), name="my_trips"),
    # path('mytrip/<uuid:schedule_id>/purchase/', views.purchase_trip, name='purchase_trip')
    # path("url/", views.my_reused_view, {"my_template_name": "some_path"}, name="aurl"),
    # path(
    #     "scheduleurl/",
    #     views.my_reused_view,
    #     {"my_template_name": "another_path"},
    #     name="scheduleurl",
    # ),
]
