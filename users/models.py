from django.db import models
from django.contrib.auth.models import User

class BaseProfile(models.Model):
    class Meta:
        abstract = True

    def upload_path(instance, filename):
		return os.path.join('games', '%d' % instance.id, 'images', filename)
		
    user = models.OneToOneField(User)
    location = models.CharField(max_length=128, null=True)
    profile_picture = models.ImageField(upload_to=upload_path, null=True)

class UserProfile(BaseProfile):
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    interested_in = models.CharField(max_length=128, null=True)
    instruments = models.CharField(max_length=128, null=True)

class MusicianProfile(BaseProfile):
    genre = models.CharField(max_length=128, null=True)

class VenueProfile(BaseProfile):
    genre = models.CharField(max_length=128, null=True)
