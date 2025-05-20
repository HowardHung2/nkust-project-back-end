from django.shortcuts import render

# Create your views here.

# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from .models import TripToken

# def token_metadata_json(request, token_id):
#     token = get_object_or_404(TripToken, order__id=token_id)

#     return JsonResponse({
#         "name": f"Trip Token #{token.token_index}",
#         "description": f"A token representing booking for {token.trip_schedule.trip.title}",
#         "image": "https://yourdomain.com/static/images/token_default.png",
#         "attributes": [
#             {"trait_type": "Country", "value": token.trip_schedule.trip.location_country},
#             {"trait_type": "City", "value": token.trip_schedule.trip.location_city},
#             {"trait_type": "Departure", "value": str(token.trip_schedule.date)},
#         ]
#     })

# management/tokens/views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from management.order.models import TripOrder  

def token_metadata_json(request, order_id):
    order = get_object_or_404(TripOrder, id=order_id)
    
    metadata = {
        "name": f"Trip Token #{order.id}",
        "description": f"Booking for: {order.trip_schedule.trip.title}",
        "attributes": {
            "trip_title": order.trip_schedule.trip.title,
            "date": str(order.trip_schedule.date),
            "location": f"{order.trip_schedule.trip.location_country}, {order.trip_schedule.trip.location_city}",
            "owner": order.user.username,
        },
        "image": "https://yourdomain.com/static/images/default_nft.jpg",  # 可選
    }

    return JsonResponse(metadata)
