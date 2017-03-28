"""uvaTextbookExchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from marketplace.models import Textbook, TextbookPost
from marketplace import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='main'),

    #API urls
    url(r'^v1/api/textbooks/$', views.getTextbooks, name="allTextbooks"),     #read
    url(r'^v1/api/textbooks/delete/$', views.deleteTextbook, name="deleteBook"), #delete
    url(r'^v1/api/textbooks/create/$', views.createTextbook, name="createTextbook"), #create
    url(r'^v1/api/textbooks/updateTextbook/$', views.updateTextbook, name="updateTextbook"), #update
    url(r'^v1/api/postTextbookByForm/', views.postTextbookByForm, name="postTextbook"), #create textbook post
    url(r'^v1/api/updateTextbookPost/$', views.updateTextbook, name="updatePost"), #update textbook post
    url(r'^v1/api/textbooklistings/', views.getTextbookPost, name="getTextbookPosts"), #read textbook posts
    url(r'^v1/api/popularListings/', views.getPopularPosts, name="getPopularPosts"),
    url(r'^v1/api/recentListings/', views.getRecentPosts, name="getRecentPosts"),
    url(r'^v1/api/login/', views.login, name="login"),
    url(r'^v1/api/createUser/', views.createUser, name="createUser"),
    url(r'^v1/api/user/', views.getUser, name="getUser"),
]
