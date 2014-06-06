from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from users.views import	MusiciansView, MusiciansProfileView, MusiciansProfileEditView, MusicianRegistrationView, MusiciansProfileAddPhoto, check_if_user

urlpatterns = patterns('',

    url(r'^$', 
        MusiciansView.as_view(),
        name='musicians'),
    url(r'^register/$', 
        MusicianRegistrationView.as_view(), 
        name='musicians_register'),
    url(r'^(?P<name>\w+)/$',
        MusiciansProfileView.as_view(),
        name='musicians_profile'),
    url(r'^(?P<name>\w+)/edit/$',
        MusiciansProfileEditView.as_view(),
        name='musicians_profile_edit'),
    url(r'^(?P<name>\w+)/add_photo/$',
        login_required(MusiciansProfileAddPhoto.as_view()),
        name='musicians_profile_add_photo'),
)
