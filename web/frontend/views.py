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
    req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/')
    allbooks = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    #return render(request, 'book_list.html', {})
    return render(request, 'book_list.html', {'book_list': allbooks['results']})

#def book_detail(request, id):
    #this_book = Books.objects.get(pk=id)
    #return render(request, 'book_list.html', {
        #'this_book' : Books.objects.get(pk = id), 'id':id})

