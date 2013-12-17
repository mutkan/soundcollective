from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from soundcollective.views import Home

urlpatterns = patterns('',

    url(r'^$', Home.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),

    # registration and sessions
	url(r'^listeners/', include('users.urls')),
	url(r'^logout/$', 
		'django.contrib.auth.views.logout_then_login', 
		name='logout'),
)
