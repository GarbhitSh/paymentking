# businesses/models.py

from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    upi_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name
