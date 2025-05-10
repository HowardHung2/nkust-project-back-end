from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

from .models import Trip, TripSchedule, TripToken
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




