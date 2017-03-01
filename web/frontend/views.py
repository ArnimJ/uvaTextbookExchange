from django.shortcuts import render
import urllib.parse
import urllib.request
import json
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
# Create your views here.

def index(request):
    #req = urllib.request.Request('http://exp-api:8000/v1/api/popularListings/')
    #popular = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    #req = urllib.request.Request('http://exp-api:8000/v1/api/recentListings/')
    #recent = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    #req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/')
    #allbooks = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))

    template = loader.get_template('index.html')
    #context = {
    #    'popular' : popular['results'],
    #    'recent' : recent['results'],
    #    'allbooks' : allbooks['results']
    #}
    #return HttpResponse(template.render(context, request))
    return render(request, 'index.html', {})

def book_list(request):
    template = loader.get_template('book_list.html')
    return render(request, 'book_list.html', {})
