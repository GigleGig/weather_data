from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f'{self.name},{self.country}'
    
class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="weather_records")
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.IntegerField(help_text="Humidity", validators=[MinLengthValidator(0), MaxLengthValidator(100)])
    wind_speed = models.FloatField(help_text="Wind Speed m/s")
    pressure = models.IntegerField(help_text="Pressure hPa")
    brief_description = models.CharField(max_length=500, help_text="Brief Description of current city weather")
    record_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-record_at']

    def __str__(self):
        return f"{self.city.name},{self.temperature}"

    @property
    def has_strong_wind(self):
        return self.wind_speed > 10
    
    @property
    def has_storm_warning(self):
        return self.pressure < 1000