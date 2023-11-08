from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    last_login = models.DateTimeField(blank=True, null=True)
    last_request = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
