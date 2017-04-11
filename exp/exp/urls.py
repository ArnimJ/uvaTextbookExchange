"""exp URL Configuration

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
from middleman import views

urlpatterns = [
    #url(r'^$', views.index, name='main'),
    url(r'^v1/api/textbooks/$', views.getTextbooks, name='textbooks'),
    url(r'^v1/api/recentListings/$', views.getRecentPosts, name='recent'),
    url(r'^v1/api/popularListings/$', views.getRecentPosts, name='popular'),
    url(r'^v1/api/allListing/$', views.getAllTextbookPosts, name='all'),
    url(r'^v1/api/login/', views.login, name="login"),
    url(r'^v1/api/logout/', views.logout, name="logout"),
    url(r'^v1/api/createUser/', views.createUser, name="signup"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^v1/api/createBuyPost/', views.createBuyPost),
    url(r'^v1/api/createSellPost/', views.createSellPost),
    url(r'^v1/api/authenticate/', views.authenticateUser),
]

