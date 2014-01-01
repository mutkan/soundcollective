from django.db import models

from uploads.models import Image
from users.models import MusicianProfile, UserProfile, VenueProfile

class MusicianImageTag(models.Model):
    image = models.ForeignKey(Image)
    tagged_musician = models.ForeignKey(MusicianProfile)

class UserImageTag(models.Model):
    image = models.ForeignKey(Image)
    tagged_user = models.ForeignKey(UserProfile)

class VenueImageTag(models.Model):
    image = models.ForeignKey(Image)
    tagged_venue = models.ForeignKey(VenueProfile)
