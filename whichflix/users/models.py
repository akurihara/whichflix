from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"


class Device(models.Model):
    device_token = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return "Device: {}".format(self.device_token)
