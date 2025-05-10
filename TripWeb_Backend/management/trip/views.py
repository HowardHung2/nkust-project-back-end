from typing import Any
from django.shortcuts import render
from .models import Trip, TripSchedule, TripToken
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










def index(request):

    num_trip = Trip.objects.all().count()
    num_tripSchedule = TripSchedule.objects.all().count()
    num_tripToken = TripToken.objects.all().count()

    num_tripSchedule_available = TripSchedule.objects.filter(status__exact='OPEN').count()
    
    context = {
        'num_trip': num_trip,
        'num_tripSchedule': num_tripSchedule,
        'num_tripToken': num_tripToken,
        'num_tripSchedule_available': num_tripSchedule_available,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

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




