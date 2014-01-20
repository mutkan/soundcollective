from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse

from posts.forms import PostForm
from posts.models import Post

from uploads.models import Image

class PostView(TemplateView):

    template_name = 'posts/posts_post.html'

    def get_object(self, queryset=None):
        obj = Post.objects.get(id=self.kwargs['post'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = self.get_object()

        try:
            context['is_user'] = True if self.get_object().created_by == self.request.user.userprofile else False
        except:
            context['is_user'] = False

        return context

class PostListView(ListView):

    model = Post
    template_name = 'posts/posts_list.html'

class PostMineView(ListView):

    template_name = 'posts/posts_list.html'
    
    def get_queryset(self):
        return Post.objects.filter(created_by=self.request.user.userprofile)

class CreatePostView(CreateView):

    model = Post
    form_class = PostForm
    template_name = 'posts/posts_create.html'

    def form_valid(self, form):
        post = form.save()

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

    def form_valid(self, form):

        image = self.get_object().flyer

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

        post = form.save()
        post.flyer = image
        post.save()

        return HttpResponseRedirect(reverse('posts_post', args=(post.id,)))
