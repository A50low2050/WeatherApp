from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Model users """

    username = models.CharField(
        "username",
        max_length=30,
        unique=True,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
