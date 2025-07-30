from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import WeatherServices
from .serializers import WeatherSerializers

class WeatherAPIView(APIView):
    """
    VIEW PART
    """

    def get(self, request):
        city_name = request.query_params.get('q')

        if not city_name:
            return Response(
                {
                    'error': 'City name is required.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        weather_data = WeatherServices.get_weather_data(city_name)

        if not weather_data["success"]:
            return Response(
                {
                    'error': 'City Weather is not recorded',
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        weather_record = WeatherServices.save_weather_data(weather_data)

        if weather_record:
            serializer = WeatherSerializers(weather_record)
            return Response(
                {
                    "successs": True,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'error':'Faied'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )