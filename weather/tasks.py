from weather_app.celery import app
from weather.models import City
from .utils import word_city
from .services import weather_service
import random


@app.task()
def get_city_api(city):
    """ Task for load data in database for work with api """

    get_city, created = City.objects.get_or_create(name=city)
    if get_city:
        return {
            "city": get_city.name,
        }
    else:
        return {
            "created": created,
        }


@app.task()
def get_cities_api():
    """ Task for get all cities in api """

    cities = word_city["city_name_en"]
    weather_info_list = []

    for city in random.sample(cities, 5):
        response = weather_service.get_weather_api(city=city)
        weather_info = {
            "city": city,
            "temp": int(response["main"]["temp"]),
            "description": response["weather"][0]["description"],
            "icon": response["weather"][0]["icon"],
        }
        weather_info_list.append(weather_info)

    return {
        "weather_info": weather_info_list
    }
