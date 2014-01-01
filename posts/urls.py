from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url

from posts.models import CreatePostView

urlpatterns = patterns('',

    url(r'^create/post/$',
        CreatePostView.as_view(),
        name='posts_create'),
        
)
