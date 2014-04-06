# encoding: utf-8
from django.db import models


class Picture(models.Model):

    def upload_path(instance, filename):
        return os.path.join('images', 'listeners', '%d' % instance.created_by.id, filename)

    file = models.ImageField(upload_to=upload_path)
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)
