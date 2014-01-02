from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from posts.views import CreatePostView, PostListView, PostView

urlpatterns = patterns('',

    url(r'^$',
        PostListView.as_view(),
        name='posts_list'),
    url(r'^create/$',
        login_required(CreatePostView.as_view()),
        name='posts_create'),
     url(r'^(?P<post>\d+)/$',
        PostView.as_view(),
        name='posts_post'),
       
)
