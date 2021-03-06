"""web URL Configuration

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
from frontend import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.book_list, name = 'book_list'),
    url(r'^book_detail/(?P<id>\d+)/$', views.book_detail, name='book_detail'),

    url(r'^register/', views.createUser, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),


    url(r'^sell/', views.selling, name = 'sell'),
    url(r'buy/', views.buying, name= 'buy'),
    url(r'^listings/', views.allListings, name='listing'),
    url(r'^listing_detail/(?P<id>\d+)/$', views.listing_detail, name='listing_detail'),
    url(r'^search_listing/', views.search_listing, name='search_listing')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
