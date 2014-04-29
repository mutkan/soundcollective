from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from posts.views import PostListView
from soundcollective.views import MainSearch
from users.views import InaccessibleView

urlpatterns = patterns('',

    url(r'^$', PostListView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^listeners/', include('users.urls')),
    url(r'^musicians/', include('users.urls_musicians')),
    url(r'^venues/', include('users.urls_venues')),

    url(r'^posts/', include('posts.urls')),	

    url(r'^logout/$', 
            'django.contrib.auth.views.logout_then_login', 
            name='logout'),
    url(r'^inaccessible/$',
            InaccessibleView.as_view(),
            name='inaccessible'),

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^search',
        MainSearch.as_view(),
        name='main_search'
    ),
)
