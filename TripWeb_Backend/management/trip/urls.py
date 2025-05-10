from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("trips/", views.TripListView.as_view(), name="trip"),
    path("trips/<uuid:pk>/", views.TripDetailView.as_view(), name="trip_detail"),
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
