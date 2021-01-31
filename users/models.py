from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    is_active = models.BooleanField()

