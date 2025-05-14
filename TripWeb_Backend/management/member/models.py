from django.db import models
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    xrpl_address = models.CharField(max_length=100, blank=True, null=True)
    xrpl_seed = models.CharField(max_length=100, blank=True, null=True)