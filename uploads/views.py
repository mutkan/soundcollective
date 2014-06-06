from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from tags.models import MusicianImageTag, UserImageTag, VenueImageTag
from uploads.models import Image
from users.models import MusicianProfile, UserProfile, VenueProfile

class UserProfileImageListView(TemplateView):

    template_name = "uploads/upload_images.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileImageListView, self).get_context_data(**kwargs)
        context['images'] = Image.filter(UserProfile__user__username=kwargs['username'])

        return context

class PhotoView(TemplateView):
    
    template_name = "uploads/photo.html"

    def post(self, request, *args, **kwargs):
        image = Image.objects.get(id=self.request.POST['photo_id'])
        image.delete()
        return HttpResponseRedirect(reverse('manage_photos', kwargs={'username': request.user.username}))

    def get_object(self, queryset=None):
        obj = Image.objects.get(id=self.kwargs['photo_id'])
        return obj
        
    def get_context_data(self, **kwargs):
        context = super(PhotoView, self).get_context_data(**kwargs)

        photo = self.get_object()
        context['photo'] = photo

        try:
            photo_tags_user = UserImageTag.filter(image=photo, tagged_user=self.request.user.userprofile)
        except:
            photo_tags_user = None

        if self.request.user.userprofile == photo.created_by or photo_tags_user:
            context['is_user'] = True

        return context
