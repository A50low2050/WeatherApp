from django.urls import path
from .views import Home, delete_weather

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("delete/<int:weather_id>/", delete_weather, name="delete_weather"),
]
