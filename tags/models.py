from django.db import models

from posts.models import Post
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

class MusicianPostTag(models.Model):
    post = models.ForeignKey(Post)
    tagged_musician = models.ForeignKey(MusicianProfile, null=True)
    string_used = models.CharField(max_length=32)

class UserPostTag(models.Model):
    post = models.ForeignKey(Post)
    tagged_user = models.ForeignKey(UserProfile, null=True)
    string_used = models.CharField(max_length=32)

class VenuePostTag(models.Model):
    post = models.ForeignKey(Post)
    tagged_venue = models.ForeignKey(VenueProfile, null=True)
    string_used = models.CharField(max_length=32)
