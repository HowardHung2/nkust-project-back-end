from rest_framework import serializers
from .models import Trip, TripSchedule

# 先做 Trip 的簡易序列化器
class TripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'trip_code', 'title', 'location_country', 'location_city', 'price_ntd']
        # 如果你有其他欄位也想輸出，可以加進來

class TripsScheduleSerializer(serializers.ModelSerializer):
    # 把 TripSchedule → 前端欄位一一對應
    trip_code = serializers.CharField(source='trip.trip_code')
    title     = serializers.CharField(source='trip.title')
    country   = serializers.CharField(source='trip.location_country')
    location  = serializers.CharField(source='trip.location_city')
    badge     = serializers.CharField(source='trip.promotions')
    image     = serializers.SerializerMethodField()
    date      = serializers.SerializerMethodField()
    price     = serializers.SerializerMethodField()

    class Meta:
        model = TripSchedule
        fields = [
            'trip_code',
            'title',
            'date',
            'country',
            'location',
            'price',
            'badge',
            'image',
        ]

    def get_image(self, obj):
        # 回傳 URL，或空字串
        if obj.trip.thumbnail:
            return obj.trip.thumbnail.url
        return ''

    def get_date(self, obj):
        # e.g. "2025/6/4~2025/6/8 5天4夜"
        start = obj.date.strftime('%Y/%-m/%-d')
        end   = obj.end_date.strftime('%Y/%-m/%-d')
        days  = (obj.end_date - obj.date).days + 1
        nights= days - 1
        return f"{start}~{end} {days}天{nights}夜"

    def get_price(self, obj):
        # e.g. "TWD$ 36,000　區區幣$ 300枚"
        ntd = f"{int(obj.price_ntd):,}"
        tokens = obj.token_index
        return f"TWD$ {ntd}　區區幣$ {tokens}枚"