from django.urls import path, include
from .views import WeatherAPIView

urlpatterns = [
    path('weather/', WeatherAPIView.as_view(), name="weather-api")
]
