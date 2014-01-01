from django.db import models

from mixins.models import CreateModifyDates

class Post(CreateModifyDates):
    
    subject = models.CharField(max_length=64, null=True)
    location = models.CharField(max_length=64, null=True)
    body = models.CharField(max_length=512, null=True)    
    date = models.DateField(null=True)
    
