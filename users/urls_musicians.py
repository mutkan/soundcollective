from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from users.views import (UserRegistrationView, login, UsersView, UserProfileView, UserProfileEditView,
	MusiciansView, MusiciansProfileView, MusiciansProfileEditView, MusicianRegistrationView, VenuesView, VenueRegistrationView)

# django-registration urls
urlpatterns = patterns('',

	# musicians
	url(r'^$', 
            MusiciansView.as_view(),
            name='users_musicians'),
	url(r'^register/$', 
            MusicianRegistrationView.as_view(), 
            name='users_musicians_register'),
        url(r'^(?P<name>\w+)/$',
            MusiciansProfileView.as_view(),
            name='users_musicians_profile'),
        url(r'^(?P<name>\w+)/edit/$',
            MusiciansProfileEditView.as_view(),
            name='users_musicians_profile_edit'),
)
