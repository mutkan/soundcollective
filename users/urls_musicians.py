from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from users.views import (UserRegistrationView, login, UsersView, UserProfileView, UserProfileEditView,
	MusiciansView, MusiciansProfileView, MusiciansProfileEditView, MusicianRegistrationView, VenuesView, VenueRegistrationView,
        MusiciansProfileViewRed, MusiciansProfileViewOld)

# django-registration urls
urlpatterns = patterns('',

	# musicians
	url(r'^$', 
            MusiciansView.as_view(),
            name='musicians'),
	url(r'^register/$', 
            MusicianRegistrationView.as_view(), 
            name='musicians_register'),
        url(r'^(?P<name>\w+)/old$',
            MusiciansProfileViewOld.as_view(),
            name='musicians_profile_old'),
        url(r'^(?P<name>\w+)/$',
            MusiciansProfileView.as_view(),
            name='musicians_profile'),
        url(r'^(?P<name>\w+)/red$',
            MusiciansProfileViewRed.as_view(),
            name='musicians_profile_red'),
        url(r'^(?P<name>\w+)/edit/$',
            MusiciansProfileEditView.as_view(),
            name='musicians_profile_edit'),
)
