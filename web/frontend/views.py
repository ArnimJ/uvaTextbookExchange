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

    #context = {
    #    'popular' : popular['results'],
    #    'recent' : recent['results'],
    #    'allbooks' : allbooks['results']
    #}
    #return HttpResponse(template.render(context, request)
    req = urllib.request.Request('http://exp-api:8000/v1/api/popularListings/')
    allposts = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/')
    allbooks = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    return render(request, 'index.html', {'postings_list': allposts['results'], 'book_list' : allbooks['results']})

def book_list(request):
    req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/')
    allbooks = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    return render(request, 'book_list.html', {'book_list': allbooks['results']})

def book_detail(request, id):
    #req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/', {'id': id})
    req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/')
    allbooks = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    return render(request, 'book_detail.html', {'book_list' : allbooks['results'], 'id': id})

