import datetime

from django.db import models

class CreateModifyDatesNoUser(models.Model):
    
    class Meta:
        abstract = True

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()

        self.modified_date = datetime.datetime.now()

        super(CreateModifyDatesNoUser, self).save(*args, **kwargs)

class CreateDates(models.Model):

    class Meta:
        abstract = True

    created_by = models.ForeignKey('users.UserProfile', related_name='%(class)s_created_by', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()

        super(CreateDates, self).save(*args, **kwargs)

class CreateModifyDates(CreateDates):

    class Meta:
        abstract = True

    modified_by = models.ForeignKey('users.UserProfile', related_name='%(class)s_modified_by', blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()

        self.modified_date = datetime.datetime.now()
        super(CreateModifyDates, self).save(*args, **kwargs)
            
    from django import template
    from django.template.defaultfilters import stringfilter
    
    register = template.Library()
    
    @register.filter
    @stringfilter
    def upto(value, delimiter=None):
        return value.split(delimiter)[0]
    upto.is_safe = True
