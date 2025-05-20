# from django.db import models
# import uuid
# from django.contrib.auth.models import User
# from management.trip.models import TripSchedule

# # Create your models here.

# class TripOrder(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     trip_schedule = models.ForeignKey(TripSchedule, on_delete=models.CASCADE)
#     spots_booked = models.IntegerField(default=1, help_text="訂購的名額數")
#     booking_date = models.DateTimeField(auto_now_add=True)
#     payment_status = models.CharField(
#         max_length=20,
#         choices=[("PENDING", "待付款"), ("PAID", "已付款"), ("CANCELLED", "已取消")],
#         default="PENDING",
#     )

#     class Meta:
#         permissions = [
#             ("can_purchase_trip", "Can purchase trip"),
#         ]

#     def __str__(self):
#         return f"{self.user.username} booked {self.spots_booked} spot(s) for {self.trip_schedule}"


# management/order/models.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User

from management.trip.models import TripSchedule
from management.tokens.models import TripToken
from TripWeb_NFT_Management.mintAndBurnNFT import mint_token



class TripOrder(models.Model):
    """
    A customer's booking of a particular TripSchedule.
    When first saved, triggers on‐chain NFT mint and records the token.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trip_orders",
        help_text="User who placed this order"
    )
    trip_schedule = models.ForeignKey(
        TripSchedule,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="Which schedule was booked"
    )
    spots_booked = models.IntegerField(
        default=1,
        help_text="Number of seats booked"
    )
    booking_date = models.DateTimeField(
        auto_now_add=True,
        help_text="When the booking was made"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("PAID", "Paid"), ("CANCELLED", "Cancelled")],
        default="PENDING",
        help_text="Payment lifecycle status"
    )

    # class Meta:
    #     permissions = [
    #         ("can_purchase_trip", "Can purchase trip"),
    #     ]

    def __str__(self):
        return f"{self.user.username} → {self.trip_schedule} ({self.spots_booked} seats)"

    # def save(self, *args, **kwargs):
    #     # Determine if this is a brand-new order
    #     is_new = self._state.adding
    #     super().save(*args, **kwargs)

    #     if is_new:
    #         # 1) Build a URI pointing to your token metadata (JSON on your server or IPFS)
    #         metadata_uri = self._build_token_metadata_uri()

    #         minter_user = User.objects.get(username="admin")
    #         minter_seed = minter_user.profile.xrpl_seed 

    #         # 2) Mint the NFT on XRPL
    #         #    flags, transfer_fee, taxon are XRPL-specific mint parameters
    #         mint_result = mint_token(
    #             seed=minter_seed,
    #             # seed=self.user.profile.xrpl_seed,
    #             uri=metadata_uri,
    #             flags=8,
    #             transfer_fee=0,
    #             taxon=0,
    #         )

    #         # 3) If mint succeeded, record a new TripToken
    #         tx_hash = (
    #             mint_result.get("hash")
    #             if isinstance(mint_result, dict)
    #             else None
    #         )

    #         if tx_hash:
    #             # next token_index is count+1
    #             next_index = (
    #                 TripToken.objects
    #                 .filter(trip_schedule=self.trip_schedule)
    #                 .count()
    #                 + 1
    #             )
    #             TripToken.objects.create(
    #                 trip_schedule=self.trip_schedule,
    #                 token_index=next_index,
    #                 owner=self.user,
    #                 order=self,
    #                 token_uri=metadata_uri,
    #                 mint_tx_hash=tx_hash,
    #                 status="ISSUED",
    #                 issued_at=timezone.now(),
    #             )
    #         else:
    #             # You might want to log or retry on failure
    #             print("⚠️ NFT mint failed:", mint_result)

    def _build_token_metadata_uri(self):
        """
        Construct a link where the token's off-chain metadata JSON lives.
        You can host this on your server or on IPFS.
        """
        # Example: reverse to a view that returns JSON for this order
        return self._absolute_url(
            reverse("token-metadata-json", args=[str(self.id)])
        )

    def _absolute_url(self, path):
        """
        Given a path, build full URL including protocol/host.
        In production, you might read SITE_DOMAIN from settings.
        """
        domain = getattr(settings, "SITE_DOMAIN", "http://localhost:8000")
        return f"{domain}{path}"
