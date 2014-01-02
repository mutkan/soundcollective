from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse

from posts.forms import PostForm
from posts.models import Post

class PostView(TemplateView):

    template_name = 'posts/posts_post.html'

    def get_object(self, queryset=None):
        obj = Post.objects.get(id=self.kwargs['post'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['is_user'] = True if self.get_object().user_profile == self.request.user.userprofile else False
        return context

class PostListView(ListView):

    model = Post
    template_name = 'posts/posts_list.html'

class CreatePostView(CreateView):

    model = Post
    form_class = PostForm
    template_name = 'posts/posts_create.html'

    def form_valid(self, form):
        post = form.save()

        post.user_profile = self.request.user.userprofile
        post.save()

        return HttpResponseRedirect(reverse('posts_post', args=(post.id,)))
