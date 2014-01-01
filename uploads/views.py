from django.shortcuts import render
from django.views.generic import TemplateView

from uploads.models import Image
from users.models import MusicianProfile, UserProfile, VenueProfile

class UserProfileImageListView(TemplateView):

	template_name = "uploads/uploads_profile_image_list.html"

	def get_context_data(self, **kwargs):
		context = super(UserProfileImageListView, self).get_context_data(**kwargs)

		context['images'] = Image.filter(UserProfile__user__username=kwargs['username'])
		return context