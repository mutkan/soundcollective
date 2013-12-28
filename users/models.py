import os

from django.db import models
from django.contrib.auth.models import User

class BaseProfile(models.Model):
    class Meta:
        abstract = True

    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=32, null=True)
    location = models.CharField(max_length=128, null=True)
    blurb = models.CharField(max_length=256, null=True)

class UserProfile(BaseProfile):

    def upload_path(instance, filename):
        return os.path.join('images', 'listeners', '%d' % instance.id, filename)

    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    interested_in = models.CharField(max_length=128, null=True)
    instruments = models.CharField(max_length=128, null=True)
    profile_image = models.ImageField(upload_to=upload_path, null=True, default='images/common/cassette.png/')
    splash_image = models.ImageField(upload_to=upload_path, null=True)

class MusicianProfile(BaseProfile):

    def upload_path(instance, filename):
        return os.path.join('images', 'musicians', '%d' % instance.id, filename)

    name = models.CharField(max_length=128, null=False)
    genre = models.CharField(max_length=128, null=True)
    profile_image = models.ImageField(upload_to=upload_path, null=True, default='images/common/cassette.png/')
    splash_image = models.ImageField(upload_to=upload_path, null=True)

class VenueProfile(BaseProfile):

    def upload_path(instance, filename):
        return os.path.join('images', 'venues', '%d' % instance.id, filename)

    name = models.CharField(max_length=128, null=False)
    genre = models.CharField(max_length=128, null=True)
    profile_image = models.ImageField(upload_to=upload_path, null=True, default='images/common/cassette.png/')
    splash_image = models.ImageField(upload_to=upload_path, null=True)
