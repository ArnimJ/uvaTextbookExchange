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
from marketplace.models import Textbook
from marketplace.models import TextbookPost

from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class TextbookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Textbook
        fields = ('title', 'isbn', 'author', 'publicationDate', 'publisher')

# ViewSets define the view behavior.
class TextbookViewSet(viewsets.ModelViewSet):
    queryset = Textbook.objects.all()
    serializer_class = TextbookSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'textbook', TextbookViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(router.urls)),
    url(r'^/api/v1/textbooks/', include('rest_framework.urls', namespace='rest_framework'))
]
