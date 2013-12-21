from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from users.views import (UserRegistrationView, login, UsersView, UserProfileView, UserProfileEditView,
	MusiciansView, MusicianRegistrationView, VenuesView, VenueRegistrationView)

# django-registration urls
urlpatterns = patterns('',

	# venues
	url(r'^$', VenuesView.as_view(), name='users_venues'),
	url(r'^$', 
		VenueRegistrationView.as_view(),
		name='users_venues'),
)
