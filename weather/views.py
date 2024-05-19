from django.conf import settings
from django.shortcuts import redirect
from django.core.cache import cache
from django.urls import reverse
from .forms import WeatherCityForm
from django.views.generic import ListView
from .models import WeatherCity
from users.models import User
from weather.services import weather_service


class Home(ListView):
    """ Home page website """

    model = WeatherCity
    form_class = WeatherCityForm
    template_name = "home/home.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            get_city = form.cleaned_data["name"].title()
            request.session["get_city"] = get_city
            response = weather_service.get_weather_api(get_city)
            user = self.request.user

            if response["cod"] in ["404", "400"]:
                return redirect(reverse("home"))

            else:
                weather = weather_service.get_weather_filter(get_city, user)

                if weather:
                    weather_service.get_weather_update(user=user, name=get_city)
                    cache.delete(settings.CACHE_CITY_NAME)
                    return super().get(request, *args, **kwargs)
                else:
                    weather_service.weather_create(user=user, name=get_city)
                    cache.delete(settings.CACHE_CITY_NAME)
                    return super().get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        get_city = self.request.session.get("get_city")
        if get_city:

            user = self.request.user
            weather_info = weather_service.get_weather_filter(city=get_city, user=user).first()
            get_cache_city = cache.get(settings.CACHE_CITY_NAME)

            if get_cache_city:
                all_cities = get_cache_city
            else:
                all_cities = weather_service.get_weathers_user_all(user=user)
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
            all_cities = weather_service.get_weathers_user_all(user=user)

            context["all_cities"] = all_cities
            context["title"] = "WeatherApp"
            context["form"] = form
            return context


def delete_weather(request, weather_id):
    """ Delete weather """

    w = WeatherCity.objects.get(pk=weather_id)
    w.delete()
    cache.delete(settings.CACHE_CITY_NAME)
    return redirect("home")
