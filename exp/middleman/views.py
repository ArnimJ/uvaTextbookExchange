import urllib.parse
import urllib.request
import json
from django.http import HttpResponse, JsonResponse

def getTextbooks(request):
    if request.method == 'GET':
        data = urllib.parse.urlencode(dict(request.GET)).encode('ascii')
        req = urllib.request.Request('http://models-api:8000/v1/api/textbooks/', data)
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        return JsonResponse(json.loads(resp_json))

def getPopularPosts(request):
    req = urllib.request.Request('http://models-api:8000/v1/api/popularListings/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return JsonResponse(json.loads(resp_json))

def getRecentPosts(request):
    req = urllib.request.Request('http://models-api:8000/v1/api/recentListings/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    return JsonResponse(json.loads(resp_json))
