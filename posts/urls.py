from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from posts.views import (CreatePostView, EditPostView, PostListView, PostMineView,
    PostView)#, CreateFeaturePost, FeaturePostView)

urlpatterns = patterns('',

    url(r'^$',
        PostListView.as_view(),
        name='posts_list'),
    url(r'^create/$',
        login_required(CreatePostView.as_view()),
        name='posts_create'),
    url(r'^mine/$',
        login_required(PostMineView.as_view()),
        name='posts_mine'),
    url(r'^(?P<post>\d+)/$',
        PostView.as_view(),
        name='posts_post'),
    url(r'^(?P<post>\d+)/edit/$',
        EditPostView.as_view(),
        name='posts_edit'),

#    url(r'^create_feature/$',
#        login_required(CreateFeaturePost.as_view()),
#        name='create_feature'),
#    url(r'^feature/(?P<post>\d+)/$',
#        FeaturePostView.as_view(),
#        name='posts_feature_post'),
)
