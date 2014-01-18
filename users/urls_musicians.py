from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from users.views import (UserRegistrationView, login, UsersView, UserProfileView, UserProfileEditView,
	MusiciansView, MusicianRegistrationView, VenuesView, VenueRegistrationView)

# django-registration urls
urlpatterns = patterns('',

	# musicians
	url(r'^$', MusiciansView.as_view(), name='users_musicians'),
	url(r'^register/$', 
		MusicianRegistrationView.as_view(), 
		name='users_musicians'),
        url(r'^(?P<name>\w+/$',
            MusicianProfileView.as_view(),
            name='users_musicians_profile'),
        url(r'^(?P<name>\w+/edit/$',
            MusicianProfileEditView.as_view(),
            name='users_musicians_profile_edit'),
)
