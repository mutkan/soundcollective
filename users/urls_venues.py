from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from users.views import VenuesView, VenueRegistrationView, VenuesProfileView 

urlpatterns = patterns('',

	url(r'^$',
            VenuesView.as_view(),
            name='venues'),
	url(r'^register/$', 
            VenueRegistrationView.as_view(),
            name='venues_registration'),
        url(r'^(?P<name>\w+)/$',
            VenuesProfileView.as_view(),
            name='venues_profile'),
)
