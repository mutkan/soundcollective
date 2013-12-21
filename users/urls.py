from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from users.views import (UserRegistrationView, login, UsersView, UserProfileView, UserProfileEditView,
	MusiciansView, MusicianRegistrationView, VenuesView, VenueRegistrationView)

# django-registration urls
urlpatterns = patterns('',

	# registration
	url(r'^activate/complete/$',
		TemplateView.as_view(template_name='registration/activation_complete.html'),
		name='registration_activation_complete'),
	url(r'^activate/(?P<activation_key>\w+)/$',
		ActivationView.as_view(),
		name='registration_activate'),
	url(r'^register/$', 
		UserRegistrationView.as_view(), 
		name='registration_register'),
	url(r'^register/complete/$',
		TemplateView.as_view(template_name='registration/registration_complete.html'),
		name='registration_complete'),
	url(r'^register/closed/$',
		TemplateView.as_view(template_name='registration/registration_closed.html'),
		name='registration_disallowed'),
	url(r'^login/$',
		login,
		name='registration_login'),
	(r'', include('registration.auth_urls')),

	# listeners
	url(r'^$', UsersView.as_view(), name='users_listeners'),
	url(r'^(?P<username>\w+)/$',
		UserProfileView.as_view(),
		name='users_listeners_profile'),
	url(r'^(?P<username>\w+)/edit/$',
		UserProfileEditView.as_view(),
		name='users_listeners_profile_edit'),

	# musicians
	url(r'^$', MusiciansView.as_view(), name='users_musicians'),
	url(r'^$', 
		MusicianRegistrationView.as_view(), 
		name='users_musicians'),

	# venues
	url(r'^$', VenuesView.as_view(), name='users_venues'),
	url(r'^$', 
		VenueRegistrationView.as_view(),
		name='users_venues'),
)
