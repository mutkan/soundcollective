from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from posts.forms import PostForm
from posts.models import Post

class PostListView(ListView):

    model = Post

class CreatePostView(CreateView):
    
    model = Post
    form_class = PostForm
