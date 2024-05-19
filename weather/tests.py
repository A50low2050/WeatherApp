import requests
import requests_mock
from django.test import TestCase
from weather.services import weather_service


class GetWeatherApiTest(TestCase):
    @requests_mock.Mocker()
    def test_get_weather_api(self, mocker):
        city = "London"
        api_url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b6e6d86335de11f4c78b701b4183dfa9"

        mock_response = {
            "coord": {"lon": -0.13, "lat": 51.51},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
            "base": "stations",
            "main": {
                "temp": 15.0,
                "feels_like": 13.7,
                "temp_min": 15.0,
                "temp_max": 15.0,
                "pressure": 1023,
                "humidity": 67
            },
            "visibility": 10000,
            "wind": {"speed": 3.1, "deg": 230},
            "clouds": {"all": 0},
            "dt": 1586468027,
            "sys": {
                "type": 1,
                "id": 1414,
                "country": "GB",
                "sunrise": 1586488128,
                "sunset": 1586537727
            },
            "timezone": 3600,
            "id": 2643743,
            "name": "London",
            "cod": 200
        }

        mocker.get(api_url.format(city), json=mock_response)

        response = weather_service.get_weather_api(city=city)
        self.assertEqual(response["name"], "London")
        self.assertEqual(response["main"]["temp"], 15.0)
        self.assertEqual(response["weather"][0]["description"], "clear sky")
