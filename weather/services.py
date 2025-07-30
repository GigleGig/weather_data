import requests
from django.conf import settings
from django.core.cache import cache
from .models import City, Weather

class WeatherServices:

    @staticmethod
    def get_weather_data(city_name):
        cache_key = f"weather_{city_name.lower()}"
        cache_data = cache.get(cache_key)

        if cache_data:
            return cache_data
        
        try:
            url = settings.OPENWEATHER_BASE_URL
            params = {
                "q": city_name,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": 'metric',
            }

            response = requests.get(url, params)
            response.raise_for_status()

            data = response.json()

            weather_data = {
                'city_name': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'pressure': data['main']['pressure'],
                'brief_description': data['weather'][0]['description'],
                'success': True
            }
            cache.set(cache_key, weather_data, timeout=600)
            return weather_data
        
        except requests.exceptions.RequestException as e:
            if cache_data:
                return cache_data
            return {
                "success": False,
                "error": "Unable to get the weather and no cached data available"
            }
        
        except requests.exceptions.Timeout:
            if cache_data:
                return cache_data
            return {
                "success": False,
                "error": "Unable to get the weather, timeout and no cached data available"
            }
        
        except Exception as e:
            if cache_data:
                return cache_data
            return {
                "success": False,
                "error": "Weather Service is currently not usable and no cached data available",
            }
        
    @staticmethod
    def save_weather_data(weather_data):
        try:
            city, created = City.objects.get_or_create(
                name = weather_data['city_name'],
                defaults={'country': weather_data['country']}
            )

            weather = Weather.objects.create(
                city = city,
                temperature = weather_data['temperature'],
                humidity= weather_data['humidity'],
                wind_speed= weather_data['wind_speed'],
                pressure= weather_data['pressure'],
                brief_description= weather_data['brief_description'],
            )

            return weather
        
        except Exception as e:
            return None 