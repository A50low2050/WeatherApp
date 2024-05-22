from django.contrib import admin
from .models import WeatherCity, City


@admin.register(WeatherCity)
class AdminWeatherCity(admin.ModelAdmin):
    """ Admin Weather """

    list_display = ["id", "name", "temp", "description", "icon", "user"]


@admin.register(City)
class AdminWeatherCity(admin.ModelAdmin):
    """ Admin City """

    list_display = ["id", "name", "created_at"]
