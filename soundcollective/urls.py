from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from soundcollective.views import Home

urlpatterns = patterns('',

    url(r'^$', Home.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),

	url(r'^listeners/', include('users.urls')),
	url(r'^musicians/', include('users.urls_musicians')),
	url(r'^venues/', include('users.urls_venues')),
	
	url(r'^logout/$', 
		'django.contrib.auth.views.logout_then_login', 
		name='logout'),
)
