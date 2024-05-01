from django.contrib import admin
from .models import WeatherCity


@admin.register(WeatherCity)
class AdminWeatherCity(admin.ModelAdmin):
    list_display = ["id", "name", "temp", "description", "icon"]
