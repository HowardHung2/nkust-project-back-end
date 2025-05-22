import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# 行程表
class Trip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip_code = models.CharField(
        max_length=100, unique=True, help_text="每個行程的唯一識別碼，例：T001、T002等"
    )  # 行程唯一識別碼
    title = models.CharField(
        max_length=255, help_text="請輸入行程的名稱，例：日本溫泉三日遊"
    )  # 行程主題
    location_country = models.CharField(
        max_length=100, help_text="請輸入行程的目的地國家名稱，例：日本"
    )  # 目的地國家
    location_city = models.CharField(
        max_length=100, help_text="請輸入行程的目的地城市名稱，例：東京"
    )  # 目的地城市
    price_ntd = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="行程的價格，預設為新台幣"
    )  # 行程價格（NTD）
    currency = models.CharField(
        max_length=10, default="TWD", help_text="幣別"
    ) # 幣別（預設為新台幣）
    min_group_size = models.IntegerField(
        help_text="此行程最少需要的成團人數"
    )  # 最少成團人數
    features = models.TextField(
        help_text="行程的特色或亮點，例：溫泉、滑雪、觀光等"
    )  # 行程特色（可用JSON格式保存）
    promotions = models.TextField(
        help_text="行程的優惠措施，例：早鳥優惠、組合套餐優惠等"
    )  # 優惠措施（可用JSON格式保存）
    flight_reference = models.TextField(
        help_text="參考航班資料，包含去程和回程的航班資訊，格式為JSON"
    )  # 參考航班（JSON格式，包含去程與回程資訊）
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    is_active  = models.BooleanField(default=True)
    thumbnail  = models.ImageField(null=True, blank=True)

    def get_absolute_url(self):
        # 生成行程的詳細頁面 URL
        return reverse("trip_detail", kwargs={"pk": str(self.id)})

    def __str__(self):
        return f"{self.title} ({self.location_country}, {self.location_city})"


# 行程日期與代幣發行數量（每個日期時段對應的代幣）
class TripSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip = models.ForeignKey(
        Trip,
        related_name="schedules",
        on_delete=models.CASCADE,
        help_text="此日期時段所屬的行程",
    )  # 行程ID（外鍵）
    date = models.DateField(help_text="行程的具體出發日期")  # 日期
    end_date = models.DateField(help_text="行程的結束日期")  # 日期
    token_index = models.IntegerField(
        help_text="此日期時段所發行的代幣數量"
    )  # 發行的代幣數量
    available_spots = models.IntegerField(
        help_text="此日期時段可預訂的名額數"
    )  # 可預訂名額
    price_ntd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="此日期時段的價格（NTD），與基本行程價格可能不同",
    )  # 該時段的價格（可根據需求區分）
    status = models.CharField(
        max_length=10,
        choices=[
            ("OPEN", "Open for Reservation"),
            ("CLOSED", "Reservation Closed"),
            ("FULL", "Sold Out"),
        ],
        default="OPEN",
        help_text="日期時段的狀態，例：開放預訂、已關閉預訂、已滿額",
    )  # 日期時段狀態

    sold_users = models.ManyToManyField(
        User,
        through='order.TripOrder',
        related_name='purchased_tripschedules',
        blank=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["trip"]),
        ]

    def __str__(self):
        return f"Trip {self.trip} Schedule on {self.date}"


