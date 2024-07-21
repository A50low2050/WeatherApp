from .models import WeatherCity
from django.forms import ModelForm, TextInput


class WeatherCityForm(ModelForm):
    """ Form for weather """
    class Meta:
        model = WeatherCity
        fields = ["name"]
        widgets = {"name": TextInput(attrs={
            "class": "form-control mr-sm-2 me-2",
            "name": "city",
            "placeholder": "City",
        })}
