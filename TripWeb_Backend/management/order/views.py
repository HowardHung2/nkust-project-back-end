from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import TripSchedule, TripOrder
from .forms import PurchaseTripForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class TripScheduleByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = TripOrder
    template_name = 'trip_schedule_list_by_user.html'
    context_object_name = 'user_trip_orders'
    paginate_by = 10

    def get_queryset(self):
        return (
            TripOrder.objects.filter(user=self.request.user)
            .select_related('trip_schedule', 'trip_schedule__trip')  # 順便抓 trip 和 trip_schedule，減少 SQL 查詢
            .order_by('-booking_date')
        )


@permission_required('management.trip.can_purchase_trip')
def purchase_trip(request, schedule_id):
    schedule = get_object_or_404(TripSchedule, pk=schedule_id)

    if request.method == 'POST':
        form = PurchaseTripForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.trip_schedule = schedule
            order.save()
            return redirect('my_order')  # 假設你有一個訂單列表頁
    else:
        form = PurchaseTripForm()

    return render(request, 'purchase_trip.html', {
        'form': form,
        'schedule': schedule,
    })

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import TripSchedule
# from order.models import TripOrder
# from .serializers import TripScheduleSerializer

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_trips(request):
#     user = request.user
#     orders = TripOrder.objects.filter(user=user)
#     schedules = [order.trip_schedule for order in orders]
#     data = TripScheduleSerializer(schedules, many=True).data
#     return Response(data)
