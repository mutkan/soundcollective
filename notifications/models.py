from django.db import models

from mixins.models import CreateDates

from users.models import UserProfile

# Create your models here.

class Notifications(CreateDates):

    user = models.ForeignKey(UserProfile, related_name='userprofile')
    message = models.CharField(max_length=128, null=True)
    viewed = models.BooleanField(default=False)
