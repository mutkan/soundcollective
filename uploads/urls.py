from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from uploads.views import PhotoView

urlpatterns = patterns('',
    url(r'^(?P<photo_id>\w+)/$',
        PhotoView.as_view(),
        name='photo'),
)
