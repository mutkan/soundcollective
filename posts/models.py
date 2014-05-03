from django.db import models

from mixins.models import CreateModifyDates
from users.models import UserProfile, VenueProfile
from uploads.models import Image

class Post(CreateModifyDates):
    
    subject = models.CharField(max_length=64, null=True)
    flyer = models.ForeignKey(Image, null=True)
    location = models.CharField(max_length=64, null=True)
    body = models.TextField(null=True)
    date = models.DateField(null=True)

    venue = models.ForeignKey(VenueProfile, null=True)
    opens = models.CharField(max_length=16, null=True)
    starts = models.CharField(max_length=16, null=True)
    cost = models.CharField(max_length=16, null=True)

class ShoutboxPost(CreateModifyDates):
    body = models.CharField(max_length=140, null=False)

#class FeaturePost(CreateModifyDates):
#    
#    subject = models.CharField(max_length=64, null=True)
#    preview_image = models.ForeignKey(Image, null=True)
#    content = HTMLField()
