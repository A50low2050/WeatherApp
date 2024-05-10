import requests
from django.conf import settings
from django.shortcuts import redirect
from django.core.cache import cache
from django.urls import reverse
from .forms import WeatherCityForm
from django.views.generic import ListView
from .models import WeatherCity
from users.models import User


class Home(ListView):
    model = WeatherCity
    form_class = WeatherCityForm
    template_name = "home/home.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            get_city = form.cleaned_data["name"].title()
            request.session["get_city"] = get_city
            api = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b6e6d86335de11f4c78b701b4183dfa9"
            response = requests.get(api.format(get_city)).json()
            user = self.request.user

            if response["cod"] in ["404", "400"]:
                return redirect(reverse("home"))
            else:
                weather = WeatherCity.objects.filter(name=get_city, user=user)
                if weather:

                    WeatherCity.objects.filter(name=get_city).update(
                        user=user,
                        name=get_city,
                        temp=int(response["main"]["temp"]),
                        description=response["weather"][0]["description"],
                        icon=response["weather"][0]["icon"],
                    )
                    cache.delete(settings.CACHE_CITY_NAME)
                    return super().get(request, *args, **kwargs)
                else:
                    WeatherCity.objects.create(
                        user=user,
                        name=get_city,
                        temp=int(response["main"]["temp"]),
                        description=response["weather"][0]["description"],
                        icon=response["weather"][0]["icon"],

                    )
                    cache.delete(settings.CACHE_CITY_NAME)
                    return super().get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        get_city = self.request.session.get("get_city")
        if get_city:

            user = self.request.user
            weather_info = WeatherCity.objects.filter(name=get_city).first()
            get_cache_city = cache.get(settings.CACHE_CITY_NAME)

            if get_cache_city:
                all_cities = get_cache_city
            else:
                all_cities = WeatherCity.objects.filter(user=user).all()
                cache.set(settings.CACHE_CITY_NAME, all_cities, 15)

            form = self.form_class()
            context["title"] = "WeatherApp"
            context["form"] = form
            context["weather_info"] = weather_info
            context["all_cities"] = all_cities
            return context
        else:
            form = self.form_class()
            user = User.objects.filter(username=self.request.user.username).first()
            all_cities = WeatherCity.objects.filter(user=user).all()

            context["all_cities"] = all_cities
            context["title"] = "WeatherApp"
            context["form"] = form
            return context


def delete_weather(request, weather_id):
    w = WeatherCity.objects.get(pk=weather_id)
    w.delete()
    cache.delete(settings.CACHE_CITY_NAME)
    return redirect("home")
