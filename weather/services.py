import requests
from .models import WeatherCity
import logging

logger = logging.getLogger("django")


class WeatherServices:

    def get_weather_api(self, city):
        try:
            api = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b6e6d86335de11f4c78b701b4183dfa9"
            response = requests.get(api.format(city)).json()
            return response
        except Exception as error:
            logger.error(error)

    def get_weather_filter(self, city, user):
        return WeatherCity.objects.filter(name=city, user=user)

    def get_weather_update(self, user, name):
        response = self.get_weather_api(city=name)
        temp = int(response["main"]["temp"])
        description = response["weather"][0]["description"]
        icon = response["weather"][0]["icon"]

        return WeatherCity.objects.filter(name=name).update(
                        user=user,
                        name=name,
                        temp=temp,
                        description=description,
                        icon=icon,
                    )

    def get_weathers_user_all(self, user):
        return WeatherCity.objects.filter(user=user).all()

    def weather_create(self, user, name):
        response = self.get_weather_api(city=name)
        temp = int(response["main"]["temp"])
        description = response["weather"][0]["description"]
        icon = response["weather"][0]["icon"]
        WeatherCity.objects.create(
            user=user,
            name=name,
            temp=temp,
            description=description,
            icon=icon,

        )


weather_service = WeatherServices()
