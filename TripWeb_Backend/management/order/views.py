from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import TripSchedule, TripOrder
from .forms import PurchaseTripForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib import messages

# test branch

class TripScheduleByUserListView(LoginRequiredMixin, generic.ListView):
    """列出當前使用者的所有訂單記錄"""
    model = TripOrder
    template_name = 'trip_schedule_list_by_user.html'
    context_object_name = 'user_trip_orders'
    paginate_by = 10

    def get_queryset(self):
        return (
            TripOrder.objects.filter(user=self.request.user)
            .select_related('trip_schedule', 'trip_schedule__trip')
            .order_by('-booking_date')
        )

# @permission_required('management.trip.can_purchase_trip')
def purchase_trip(request, schedule_id):
    schedule = get_object_or_404(TripSchedule, pk=schedule_id)

    if request.method == 'POST':
        form = PurchaseTripForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.trip_schedule = schedule
            order.save()
            messages.success(request, "✅ 您的預訂已成功送出！我們將盡快與您聯繫")
            return redirect('my_order')  
        else:
            messages.error(request, "⚠ 請確認表單內容是否正確")
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
