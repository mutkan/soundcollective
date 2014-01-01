import os

from django.db import models
from django.contrib.auth.models import User

from mixins.models import CreateModifyDates

class BaseProfile(CreateModifyDates):

    class Meta:
        abstract = True

    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=32, null=True)
    location = models.CharField(max_length=128, null=True)
    blurb = models.CharField(max_length=256, null=True)

class UserProfile(BaseProfile):

    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    interested_in = models.CharField(max_length=128, null=True)
    instruments = models.CharField(max_length=128, null=True)
    profile_image = models.ForeignKey('uploads.Image', related_name='user_profile_image')
    splash_image = models.ForeignKey('uploads.Image', related_name='user_splash_image')

class MusicianProfile(BaseProfile):

    name = models.CharField(max_length=128, null=False)
    genre = models.CharField(max_length=128, null=True)
    profile_image = models.ForeignKey('uploads.Image', related_name='musician_profile_image')
    splash_image = models.ForeignKey('uploads.Image', related_name='musician_splash_image')

class VenueProfile(BaseProfile):

    name = models.CharField(max_length=128, null=False)
    genre = models.CharField(max_length=128, null=True)
    profile_image = models.ForeignKey('uploads.Image', related_name='venue_profile_image')
    splash_image = models.ForeignKey('uploads.Image', related_name='venue_splash_image')

