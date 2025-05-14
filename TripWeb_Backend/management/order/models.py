from django.db import models
import uuid
from django.contrib.auth.models import User
from management.trip.models import TripSchedule

# Create your models here.

class TripOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_schedule = models.ForeignKey(TripSchedule, on_delete=models.CASCADE)
    spots_booked = models.IntegerField(default=1, help_text="訂購的名額數")
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[("PENDING", "待付款"), ("PAID", "已付款"), ("CANCELLED", "已取消")],
        default="PENDING",
    )

    class Meta:
        permissions = [
            ("can_purchase_trip", "Can purchase trip"),
        ]

    def __str__(self):
        return f"{self.user.username} booked {self.spots_booked} spot(s) for {self.trip_schedule}"
