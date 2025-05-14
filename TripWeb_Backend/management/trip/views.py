from django.shortcuts import render
from django.views import generic
from .models import Trip, TripSchedule

#TEST

def index(request):
    # 1) Basic statistics
    num_trip = Trip.objects.count()
    num_tripSchedule = TripSchedule.objects.count()
    # num_tripToken = TripToken.objects.count()
    num_tripSchedule_available = TripSchedule.objects.filter(status='OPEN').count()

    # 2) Get recommended trips (open for booking, active trips, sorted by date, limited to 3)
    recommended_schedules = (
        TripSchedule.objects
        .filter(status='OPEN', trip__is_active=True)
        .select_related('trip')      # Optimize: preload trip data to reduce SQL queries
        .order_by('date')[:3]        # Sort by departure date and take top 3
    )

    # 3) Get Departure and Destination

    context = {
        'num_trip': num_trip,
        'num_tripSchedule': num_tripSchedule,
        # 'num_tripToken': num_tripToken,
        'num_tripSchedule_available': num_tripSchedule_available,
        'recommended_schedules': recommended_schedules,
    }
    return render(request, 'index.html', context)


class TripListView(generic.ListView):
    model = Trip
    context_object_name = 'TripList'
    queryset = Trip.objects.all()[:10]
    template_name = 'triplist.html'
    paginate_by = 10

    def get_queryset(self):
        # Optional debug log
        print(f"get_queryset: {Trip.objects.all()[:10]}")
        return Trip.objects.all()[:10]

    def get_context_data(self, **kwargs):
        # first get the default context (which includes 'trip')
        context = super().get_context_data(**kwargs)
        trip = self.object  # this is the Trip instance

        # fetch all schedules for this trip (you can filter by status if you like)
        schedules = trip.schedules.all().order_by('date')

        # add into the template context
        context['schedules'] = schedules
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(TripListView, self).get_context_data(**kwargs)
    #     # Optional debug log
    #     print(f"context: {context}")
    #     return context

class TripScheduleListView(generic.ListView):
    model = TripSchedule
    context_object_name = 'TripScheduleList'
    queryset = TripSchedule.objects.all()[:10]
    template_name = 'trip_schedule_list.html'
    paginate_by = 10

class TripDetailView(generic.DetailView):
    model = Trip
    context_object_name = 'trip'
    template_name = 'triplist_detail.html'

class TripScheduleDetailView(generic.DeleteView):
    model = TripSchedule
    context_object_name = 'tripschedule'
    template_name = 'trip_schedule_detail.html'




""" 

未整理的程式碼

def index(request):
    # 1) 一些統計
    num_trip = Trip.objects.count()
    num_tripSchedule = TripSchedule.objects.count()
    num_tripToken = TripToken.objects.count()
    num_tripSchedule_available = TripSchedule.objects.filter(status='OPEN').count()

    # 2) 取熱門推薦（例如：開放預訂、active trip、依出發日排序，取前三筆）
    recommended_schedules = (
        TripSchedule.objects
        .filter(status='OPEN', trip__is_active=True)
        .select_related('trip')                # 預先抓 trip 減少 SQL
        .order_by('date')[:3]                  # 依出發日排序，取前 3 筆
    )

    context = {
        'num_trip': num_trip,
        'num_tripSchedule': num_tripSchedule,
        'num_tripToken': num_tripToken,
        'num_tripSchedule_available': num_tripSchedule_available,
        'recommended_schedules': recommended_schedules,
    }
    return render(request, 'index.html', context)

    # num_trip = Trip.objects.all().count()
    # num_tripSchedule = TripSchedule.objects.all().count()
    # num_tripToken = TripToken.objects.all().count()

    # num_tripSchedule_available = TripSchedule.objects.filter(status__exact='OPEN').count()
    
    # context = {
    #     'num_trip': num_trip,
    #     'num_tripSchedule': num_tripSchedule,
    #     'num_tripToken': num_tripToken,
    #     'num_tripSchedule_available': num_tripSchedule_available,
    # }

    # # Render the HTML template index.html with the data in the context variable
    # return render(request, 'index.html', context=context)

# def trip(request):
#     previewTrips = Trip.objects.filter()[:10]
#     previewTripsList = previewTrips.values()
    
#     context = {
#         'previewTripsList': previewTripsList
#     }
    
#     print(context)
#     return render(request, 'triplist.html', context=context)

from django.views import generic
class TripListView(generic.ListView):
    model = Trip
    context_object_name = 'TripList'
    queryset = Trip.objects.filter()[:10]
    template_name = 'triplist.html'
    paginate_by = 2
    def get_queryset(self):
        print(f"get_queryset: {Trip.objects.filter()[:10]}")
        return Trip.objects.filter()[:10]
    def get_context_data(self, **kwargs):
        context = super(TripListView, self).get_context_data(**kwargs)
        # context['some_data'] = 'This is just some data'
        print(f"context: {context}")
        return context
    
class TripDetailView(generic.DetailView):
    model = Trip
    context_object_name = 'trip'
    template_name = 'triplist_detail.html'
    # def get_object(self):
    #     try:
    #         context = Trip.objects.get(pk=self.kwargs['pk'])
    #         print(context)
    #         return context
    #     except Trip.DoesNotExist:
    #         raise Http404('Trip does not exist')
    # def get_context_data(self, **kwargs):
    #     context = super(TripDetailView, self).get_context_data(**kwargs)
    #     print(f"context: {context}")
    #     return context

"""




"""
# API 相關程式（目前未使用）

from .serializers import TripsSerializer, TripsScheduleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics

@api_view(['GET'])
def get_trips(request):
    trip = Trip.objects.all()
    data = TripsSerializer(trip, many=True).data
    return Response(data)

class get_trips_api_schedule(generics.ListAPIView):
    queryset = TripSchedule.objects.filter(trip__is_active=True)
    serializer_class = TripsScheduleSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        tour_dict = {
            item['trip_code']: {
                k: v for k, v in item.items() if k != 'trip_code'
            } for item in response.data
        }
        return Response(tour_dict)

"""