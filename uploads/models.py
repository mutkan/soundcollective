import os

from django.db import models

from mixins.models import CreateModifyDates

class Image(CreateModifyDates):

    def upload_path(instance, filename):
        return os.path.join('images', 'listeners', '%d' % instance.created_by.id, filename)
    
    image = models.ImageField(upload_to=upload_path, null=True, default='images/common/cassette.png')
