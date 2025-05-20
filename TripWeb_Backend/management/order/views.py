from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import TripSchedule, TripOrder, TripToken
from .forms import PurchaseTripForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib import messages
from django.utils import timezone  

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from TripWeb_NFT_Management.mintAndBurnNFT import mint_token

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


def purchase_trip(request, schedule_id):
    """
    Handle booking form. On success, save a TripOrder,
    mint its NFT, and record a TripToken.
    """
    schedule = get_object_or_404(TripSchedule, pk=schedule_id)

    if request.method == 'POST':
        form = PurchaseTripForm(request.POST)
        if form.is_valid():
            # 1) create the order
            order = form.save(commit=False)
            order.user = request.user
            order.trip_schedule = schedule
            order.save()

            # 2) build a metadata URI for this order
            metadata_uri = request.build_absolute_uri(
                f"/api/tokens/metadata/{order.id}/"
            )

            # 3) mint on XRPL
            print("⚠️ mint_token: using seed =", request.user.profile.xrpl_seed)
            print("⚠️ mint_token: metadata_uri =", metadata_uri)
            result = mint_token(
                seed='sEdVg2RhrZwhiJfjY6PhVbB5ZwVYrbW',
                uri=metadata_uri,
                flags=8,          # as per your protocol
                transfer_fee=0,
                taxon=0,
            )

            # 4) if mint succeeded, record the TripToken
            tx_hash = result.get("hash") if isinstance(result, dict) else None
            if tx_hash:
                next_index = (
                    TripToken.objects
                    .filter(trip_schedule=schedule)
                    .count()
                    + 1
                )
                TripToken.objects.create(
                    trip_schedule=schedule,
                    token_index=next_index,
                    owner=request.user,
                    order=order,
                    token_uri=metadata_uri,
                    mint_tx_hash=tx_hash,
                    status="ISSUED",
                    issued_at=timezone.now(),
                )
                messages.success(request, "✅ Booking confirmed & token minted!")
            else:
                messages.warning(request, "⚠️ Booking confirmed but token mint failed.")

            return redirect('my_order')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = PurchaseTripForm()

    return render(request, 'purchase_trip.html', {
        'form': form,
        'schedule': schedule,
    })




# @permission_required('management.trip.can_purchase_trip')
# def purchase_trip(request, schedule_id):
#     schedule = get_object_or_404(TripSchedule, pk=schedule_id)

#     if request.method == 'POST':
#         form = PurchaseTripForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.trip_schedule = schedule
#             order.save()
#             messages.success(request, "✅ 您的預訂已成功送出！我們將盡快與您聯繫")
#             return redirect('my_order')  
#         else:
#             messages.error(request, "⚠ 請確認表單內容是否正確")
#     else:
#         form = PurchaseTripForm()

#     return render(request, 'purchase_trip.html', {
#         'form': form,
#         'schedule': schedule,
#     })

# # from management.tokens.xrpl_nft import mint_token  # 調整成你的實際檔案路徑
# from django.utils import timezone

# class TripOrder(models.Model):
#     # ... 你原本的欄位 ...
    
#     def save(self, *args, **kwargs):
#         is_new = self._state.adding
#         super().save(*args, **kwargs)

#         if is_new:
#             # 執行 mint
#             user_profile = self.user.profile
#             seed = user_profile.xrpl_seed
#             uri = f"https://yourdomain.com/token/{self.id}"  # 可替換成實際 metadata URI
#             result = mint_token(seed=seed, uri=uri, flags=8, transfer_fee=0, taxon=0)

#             if isinstance(result, dict) and "hash" in result:
#                 # 建立 TripToken 並記錄資料
#                 from management.tokens.models import TripToken
#                 TripToken.objects.create(
#                     trip_schedule=self.trip_schedule,
#                     token_index=TripToken.objects.filter(trip_schedule=self.trip_schedule).count() + 1,
#                     owner=self.user,
#                     order=self,
#                     token_uri=uri,
#                     mint_tx_hash=result["hash"],
#                     status="ISSUED",
#                     issued_at=timezone.now()
#                 )


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
