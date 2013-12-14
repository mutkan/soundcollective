from django.db import models
from django.contrib.auth.models import User

class BaseProfile(models.Model):
    class Meta:
        abstract = True

    user = models.OneToOneField(User)
    location = models.CharField(max_length=128, null=True)
    profile_picture = models.ImageField(upload_to=None, null=True)

class UserProfile(BaseProfile):
    interested_in = models.CharField(max_length=128, null=True)
    instruments = models.CharField(max_length=128, null=True)

class MusicianProfile(BaseProfile):
    genre = models.CharField(max_length=128, null=True)

class VenueProfile(BaseProfile):
    genre = models.CharField(max_length=128, null=True)
