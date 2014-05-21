import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse

from notifications.models import Notifications

from posts.forms import PostForm#, CreateFeatureForm
from posts.models import Post#, FeaturePost

from tags.models import MusicianPostTag, UserPostTag, VenuePostTag

from uploads.models import Image

from users.models import UserProfile, MusicianProfile, VenueProfile

class PostView(TemplateView):

    template_name = 'posts/posts_post.html'

    def get_object(self, queryset=None):
        obj = Post.objects.get(id=self.kwargs['post'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        post = self.get_object()

        context['post'] = post
        context['musician_tags'] = MusicianPostTag.objects.filter(post=post)
        context['venue_tags'] = VenuePostTag.objects.filter(post=post)

        if self.request.user.is_authenticated():
            context['attending'] = self.request.user.userprofile.shows_attended.filter(id=post.id).exists()

        try:
            context['is_user'] = True if self.get_object().created_by == self.request.user.userprofile else False
        except:
            context['is_user'] = False

        return context

class PostListView(ListView):

    model = Post
    template_name = 'posts/posts_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        context['dates_list'] = Post.objects.values_list('date', flat=True).distinct()
        
        if self.request.user.is_authenticated():
            context['musician_profiles'] = self.request.user.userprofile.musicianprofile.all()
            context['venue_profiles'] = self.request.user.userprofile.venueprofile.all()

        return context

class PostMineView(ListView):

    template_name = 'posts/posts_list.html'
    
    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user.userprofile)

    def get_context_data(self, **kwargs):
        context = super(PostMineView, self).get_context_data(**kwargs)

        context['dates_list'] = self.get_queryset().values_list('date', flat=True).distinct()
        
        if self.request.user.is_authenticated():
            context['musician_profiles'] = self.request.user.userprofile.musicianprofile.all()
            context['venue_profiles'] = self.request.user.userprofile.venueprofile.all()

        return context

class CreatePostView(CreateView):

    model = Post
    form_class = PostForm
    template_name = 'posts/posts_create.html'

    def get_context_data(self, **kwargs):
        context = super(CreatePostView, self).get_context_data(**kwargs)

        musicians = MusicianProfile.objects.all().values_list('username', flat=True)
        musicians_json = json.dumps(list(musicians), cls=DjangoJSONEncoder)
        context['musicians'] = musicians_json
        venues = VenueProfile.objects.all().values_list('username', flat=True)
        venues_json = json.dumps(list(venues), cls=DjangoJSONEncoder) 
        context['venues'] = venues_json

        return context

    def form_valid(self, form):

        post = form.save()

        musician_tags = form.cleaned_data['musicians'].split(',')
        for musician_tag in musician_tags:
            try:
                musician = MusicianProfile.objects.get(username=musician_tag)
                tag = MusicianPostTag.objects.create(post=post, tagged_musician=musician, string_used=musician_tag)
                tag.save()

                message = "%s has been tagged in an event post." % musician.display_name
                for user in musician.user_profiles.all():
                    Notifications.objects.create(user=user, message=message)
            except:
                tag = MusicianPostTag.objects.create(post=post, string_used=musician_tag)
                tag.save()

        venue_tags = form.cleaned_data['venues'].split(',')
        for venue_tag in venue_tags:
            try:
                venue = VenueProfile.objects.get(username=venue_tag)
                tag = VenuePostTag.objects.create(post=post, tagged_venue=venue, string_used=venue_tag)
                tag.save()

                message = "%s has been tagged in an event post." % venue.display_name
                for user in venue.user_profiles.all():
                    Notifications.objects.create(user=user, message=message)
            except:
                tag = VenuePostTag.objects.create(post=post, string_used=venue_tag)
                tag.save()

        try: 
            flyer = self.request.FILES['flyer']
            image = Image.objects.create()
            image.created_by = self.request.user.userprofile
            image.modified_by = self.request.user.userprofile
            image.image = flyer 
            image.save()
            post.flyer = image 
        except:
            pass

        post.created_by = self.request.user.userprofile
        post.modified_by = self.request.user.userprofile
        post.save()

        return HttpResponseRedirect(reverse('posts_post', args=(post.id,)))

class EditPostView(UpdateView):
    
    model = Post
    form_class = PostForm
    template_name = 'posts/posts_create.html'

    def get_object(self, queryset=None):
        post = Post.objects.get(id=self.kwargs['post'])
        return post

    def get_context_data(self, **kwargs):
        context = super(EditPostView, self).get_context_data(**kwargs)

        musicians = MusicianProfile.objects.all().values_list('username', flat=True)
        musicians_json = json.dumps(list(musicians), cls=DjangoJSONEncoder)
        context['musicians'] = musicians_json
        venues = VenueProfile.objects.all().values_list('username', flat=True)
        venues_json = json.dumps(list(venues), cls=DjangoJSONEncoder) 
        context['venues'] = venues_json

        return context

    def form_valid(self, form):

        image = self.get_object().flyer

        post = form.save()
        post.flyer = image
        post.save()

        try: 
            flyer = self.request.FILES['flyer']
            image = Image.objects.create()
            image.created_by = self.request.user.userprofile
            image.modified_by = self.request.user.userprofile
            image.image = flyer 
            image.save()
            post.flyer = image 
        except:
            pass

        musician_tags = form.cleaned_data['musicians'].split(',')
        for musician_tag in musician_tags:
            try:
                musician = MusicianProfile.objects.get(username=musician_tag)
                tag = MusicianPostTag.objects.create(post=post, tagged_musician=musician, string_used=musician_tag)
                tag.save()

                message = "%s has been tagged in an event post." % musician.display_name
                for user in musician.user_profiles.all():
                    Notifications.objects.create(user=user, message=message)
            except:
                tag = MusicianPostTag.objects.create(post=post, string_used=musician_tag)
                tag.save()

        venue_tags = form.cleaned_data['venues'].split(',')
        for venue_tag in venue_tags:
            try:
                venue = VenueProfile.objects.get(username=venue_tag)
                tag = VenuePostTag.objects.create(post=post, tagged_venue=venue, string_used=venue_tag)
                tag.save()

                message = "%s has been tagged in an event post." % venue.display_name
                for user in venue.user_profiles.all():
                    Notifications.objects.create(user=user, message=message)
            except:
                tag = VenuePostTag.objects.create(post=post, string_used=venue_tag)
                tag.save()

        post.save()

        return HttpResponseRedirect(reverse('posts_post', args=(post.id,)))

def attend_post_view(request, post):
    
    post = Post.objects.get(id=post)
    
    user_profile = request.user.userprofile
    if user_profile.shows_attended.filter(id=post.id).exists():
        user_profile.shows_attended.remove(post)
    else:
        user_profile.shows_attended.add(post)

    return HttpResponseRedirect(reverse('posts_post', args=(post.id,)))
