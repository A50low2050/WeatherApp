from django.db import models


class WeatherCity(models.Model):
    name = models.CharField("Name City", max_length=70)
    temp = models.IntegerField("Temperature", blank=False, null=True)
    description = models.TextField("Description", blank=False, null=True)
    icon = models.CharField("ID Icon", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(WeatherCity, self).save(*args, **kwargs)

    class Meta:
        db_table = "weathers"
        ordering = ["-created_at"]
