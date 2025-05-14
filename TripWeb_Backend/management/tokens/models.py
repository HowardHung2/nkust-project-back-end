import uuid
from django.db import models
from management.trip.models import TripSchedule

# Create your models here.
# 行程代幣表


class TripToken(models.Model):
    # 定義狀態選項
    STATUS_CHOICES = [
        ("UNISSUED", "尚未發行"),
        ("ISSUED", "已發行"),
        ("SOLD_OUT", "已售罄"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip_schedule = models.ForeignKey(
        TripSchedule,
        related_name="tokens",
        on_delete=models.CASCADE,
        help_text="此代幣所屬的日期時段",
    )  # 具體的日期時段ID（外鍵）
    token_amount = models.IntegerField(help_text="此日期時段發行的第 x 顆代幣")  # 代幣數量
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="UNISSUED",  # 默認狀態是“尚未發行”
        help_text="代幣的狀態，例：尚未發行、已發行、已售罄",
    )  # 代幣狀態（例如：尚未發行、已發行、已售罄）

    def __str__(self):
        return f"Trip {self.trip_schedule.trip} Token {self.token_amount} ({self.get_status_display()})"

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status)

