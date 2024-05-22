from weather_app.celery import app
from weather.models import City


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
