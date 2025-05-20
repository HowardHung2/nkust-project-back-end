# import uuid
# from django.db import models
# from management.trip.models import TripSchedule

# # Create your models here.
# # 行程代幣表


# class TripToken(models.Model):
#     # 定義狀態選項
#     STATUS_CHOICES = [
#         ("UNISSUED", "尚未發行"),
#         ("ISSUED", "已發行"),
#         ("SOLD_OUT", "已售罄"),
#     ]
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     trip_schedule = models.ForeignKey(
#         TripSchedule,
#         related_name="tokens",
#         on_delete=models.CASCADE,
#         help_text="此代幣所屬的日期時段",
#     )  # 具體的日期時段ID（外鍵）
#     token_amount = models.IntegerField(help_text="此日期時段發行的第 x 顆代幣")  # 代幣數量
#     status = models.CharField(
#         max_length=10,
#         choices=STATUS_CHOICES,
#         default="UNISSUED",  # 默認狀態是“尚未發行”
#         help_text="代幣的狀態，例：尚未發行、已發行、已售罄",
#     )  # 代幣狀態（例如：尚未發行、已發行、已售罄）

#     def __str__(self):
#         return f"Trip {self.trip_schedule.trip} Token {self.token_amount} ({self.get_status_display()})"

#     def get_status_display(self):
#         return dict(self.STATUS_CHOICES).get(self.status)

# # order/models.py

# import uuid
# from django.db import models
# from django.conf import settings
# from management.trip.models import TripSchedule
# # from management.order.models import TripOrder
# class TripToken(models.Model):

import uuid
from django.db import models
from django.conf import settings
from management.trip.models import TripSchedule


class TripToken(models.Model):
    # Token lifecycle status choices
    STATUS_CHOICES = [
        ("UNISSUED", "Not Minted"),
        ("ISSUED", "Minted"),
        ("SOLD", "Sold"),
    ]

    # Unique identifier for each token
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary key"
    )

    # Foreign key linking this token to a specific TripSchedule
    trip_schedule = models.ForeignKey(
        TripSchedule,
        related_name="tokens",
        on_delete=models.CASCADE,
        help_text="Which schedule this token belongs to"
    )

    # Index/order of this token within the trip schedule
    token_index = models.PositiveIntegerField(
        default=1,
        help_text="Sequence number of this token within its TripSchedule, starting at 1"
    )

    # The user who owns this token
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_tokens",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who purchased this token"
    )

    # The order through which this token was sold
    order = models.ForeignKey(
        "order.TripOrder",
        related_name="tokens",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The TripOrder that resulted in this token being sold"
    )

    # URI for token metadata (typically for NFTs)
    token_uri = models.URLField(
        blank=True,
        help_text="URI to token metadata on chain (for NFTs)"
    )

    # Lifecycle status of the token
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="UNISSUED",
        help_text="Lifecycle status of the token"
    )

    # Blockchain mint transaction hash
    mint_tx_hash = models.CharField(
        max_length=128,
        blank=True,
        help_text="Blockchain transaction hash for minting"
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Record creation timestamp"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Record last update timestamp"
    )
    issued_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when token was minted"
    )
    sold_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when token was sold"
    )

    class Meta:
        verbose_name = "Trip Token"
        verbose_name_plural = "Trip Tokens"
        ordering = ("trip_schedule", "token_index")
        unique_together = ("trip_schedule", "token_index")
        indexes = [
            models.Index(fields=["trip_schedule", "status"]),
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return f"{self.trip_schedule} - Token #{self.token_index} ({self.get_status_display()})"
