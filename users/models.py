import os

from django.db import models
from django.contrib.auth.models import User

from mixins.models import CreateModifyDates, CreateModifyDatesNoUser

class BaseProfile(CreateModifyDates):

    class Meta:
        abstract = True

    display_name = models.CharField(max_length=32, null=True)
    location = models.CharField(max_length=128, null=True, default='')
    blurb = models.CharField(max_length=256, null=True)
    embedded_player = models.CharField(max_length=512, null=True)

class UserProfile(CreateModifyDatesNoUser):

    display_name = models.CharField(max_length=32, null=True)
    location = models.CharField(max_length=128, null=True, default='')
    blurb = models.CharField(max_length=256, null=True)

    user = models.OneToOneField(User, related_name='userprofile')
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    interested_in = models.CharField(max_length=128, null=True)
    instruments = models.CharField(max_length=128, null=True)
    profile_image = models.ForeignKey('uploads.Image', related_name='user_profile_image', null=True, default=1)
    shoutbox_posts = models.ManyToManyField('posts.ShoutboxPost', related_name='user_shoutbox_posts')

    embedded_player = models.CharField(max_length=512, null=True)

    contact_twitter = models.CharField(max_length=128, null=True)
    contact_facebook = models.CharField(max_length=128, null=True)

class MusicianProfile(BaseProfile):

    username = models.CharField(max_length=128, null=False)
    genre = models.CharField(max_length=128, null=True)
    profile_image = models.ForeignKey('uploads.Image', related_name='musician_profile_image', null=True, default=1)
    shoutbox_posts = models.ManyToManyField('posts.ShoutboxPost', related_name='musician_shoutbox_posts')
    user_profiles = models.ManyToManyField(UserProfile, related_name='%(class)s')

    contact_email = models.CharField(max_length=128, null=True)
    contact_twitter = models.CharField(max_length=128, null=True)
    contact_facebook = models.CharField(max_length=128, null=True)

class VenueProfile(BaseProfile):

    username = models.CharField(max_length=128, null=False)
    genre = models.CharField(max_length=128, null=True)
    profile_image = models.ForeignKey('uploads.Image', related_name='venue_profile_image', null=True, default=1)
    shoutbox_posts = models.ManyToManyField('posts.ShoutboxPost', related_name='venue_shoutbox_posts')
    user_profiles = models.ManyToManyField(UserProfile, related_name='%(class)s')

    contact_email = models.CharField(max_length=128, null=True)
    contact_twitter = models.CharField(max_length=128, null=True)
    contact_facebook = models.CharField(max_length=128, null=True)
