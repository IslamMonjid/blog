"""OMC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, static
from django.contrib import admin
from rest_framework import routers, viewsets
from rest_framework import generics
from backend.views import *

#UserView, FriendView, ProfileView, CityView, UserCheckView, UserViewSet, FriendViewSet, ProfileViewSet, CityViewSet, StateViewSet, ResendActivationMailView, ProfilePercentageView, AdView , UserActionView


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^api/', include('djoser.urls')),
	url(r'^o/', include('oauth2_provider.urls', namespace='oauths2_provider')),
	url(r'^admin/', admin.site.urls),
	url(r'^api/adminblog/', AdminBlogView.as_view()),
	url(r'^api/blog/', BlogView.as_view()),
	url(r'^api/blogusers/(?P<pk>.+)/$', BlogUsersView.as_view()),
	url(r'^api/blogposts/(?P<pk>.+)/$', BlogPostView.as_view()),
	url(r'^api/userposts/(?P<pk>.+)/$', UserPostView.as_view()),
	url(r'^api/registertoblog/', RegisterUserToBlogView.as_view()),
	url(r'^api/createpost/', PostView.as_view()),
	url(r'^api/getposts/(?P<pk>.+)/$', PostView.as_view()),
	url(r'^api/updatepost/(?P<pk>.+)/$', PostView.as_view()),
	url(r'^api/deletepost/(?P<pk>.+)/$', PostView.as_view()),
	url(r'^api/createcomment/', CommentView.as_view()),
	url(r'^api/getcomments/(?P<pk>.+)/$', CommentView.as_view()),
	url(r'^api/updatecomment/(?P<pk>.+)/$', CommentView.as_view()),
	url(r'^api/deletecomment/(?P<pk>.+)/$', CommentView.as_view()),
	url(r'^api/getcommentofuser/(?P<pk>.+)/$', GetCommentsForUSerView.as_view()),
	url(r'^api/likepost/', LikePostView.as_view()),
	url(r'^api/likecomment/', LikeCommentView.as_view()),
]

