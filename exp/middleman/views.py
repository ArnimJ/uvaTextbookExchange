import urllib.parse
import urllib.request
import json
from django.http import HttpResponse, JsonResponse
import requests
from django.contrib.auth import hashers

MODELS = 'http://models-api:8000/v1/api/'

def getTextbooks(request):
    if request.method == 'GET':
        data = urllib.parse.urlencode(dict(request.GET))
        req = urllib.request.Request(MODELS + 'textbooks/?' + data)
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        return JsonResponse(json.loads(resp_json))

def getPopularPosts(request):
    req = urllib.request.Request(MODELS + 'popularListings/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return JsonResponse(json.loads(resp_json))

def getRecentPosts(request):
    req = urllib.request.Request(MODELS + 'recentListings/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return JsonResponse(json.loads(resp_json))

def createBuyPost(request):
    resp = requests.post(MODELS + 'createBuyPost/', request.POST)
    return JsonResponse(resp.json())

def createSellPost(request):
    resp = requests.post(MODELS + 'createSellPost/', request.POST)
    return JsonResponse(resp.json())

def createUser(request):
    resp = requests.post(MODELS + 'createUser/', request.POST)
    return JsonResponse(resp.json())

def login(request):
    resp = requests.post(MODELS + 'login', request.POST)
    return JsonResponse(resp.json())

