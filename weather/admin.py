from django.contrib import admin
from .models import City, Weather

# Register your models here.

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name','country','created_at']
    search_fields = ['name','country']

@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ['city','temperature','humidity','wind_speed','pressure','brief_description','record_at']
    list_filter = ['record_at','city']
    readonly_fields = ['record_at']
