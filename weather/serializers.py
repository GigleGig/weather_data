from rest_framework import serializers
from .models import Weather, City

class WeatherSerializers(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    country = serializers.CharField(source='city.country', read_only=True)
    has_strong_wind = serializers.BooleanField(read_only=True)
    has_storm_warning = serializers.BooleanField(read_only=True)

    class Meta:
        model = Weather
        fields = [
            'city_name',
            'country',
            'temperature',
            'humidity',
            'wind_speed',
            'pressure',
            'brief_description',
            'record_at',
            'has_strong_wind',
            'has_storm_warning',
        ]