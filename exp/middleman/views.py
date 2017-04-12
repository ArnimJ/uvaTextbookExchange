import urllib.parse
import urllib.request
import json
from django.http import HttpResponse, JsonResponse
import requests
from kafka import KafkaProducer
from django.contrib.auth import hashers
import pdb
from elasticsearch import Elasticsearch

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

def getAllTextbookPosts(request): #get all textbooks
    resp = requests.get(MODELS + 'textbooklistings/', request.GET)
    return JsonResponse(resp.json())

def createBuyPost(request):
    resp = requests.post(MODELS + 'createBuyPost/', request.POST)
    return JsonResponse(resp.json())

def createSellPost(request):
    resp = requests.post(MODELS + 'createSellPost/', request.POST).json()
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    #put a dictionary of the textbook info in the post info in place of the id so that it is indexed too
    resp['data']['textbook'] = requests.post(MODELS + 'textbooks/?id='+resp['data']['textbook']).json().get('results')
    producer.send('new-listings-topic', json.dumps(resp['data']).encode('utf-8'))
    return JsonResponse(resp.json())

def createUser(request):
    resp = requests.post(MODELS + 'createUser/', request.POST)
    return JsonResponse(resp.json())

def login(request):
    resp = requests.post(MODELS + 'login/', request.POST)
    return JsonResponse(resp.json())

def logout(request):
    resp = requests.post(MODELS + 'logout/', request.POST)
    return JsonResponse(resp.json())

# def login_required(f):
#     def wrap(request, *args, **kwargs):
#
#         # try authenticating the us_validateer
#         user = authenticateUser(request)
#
#
#         # authentication failed
#         if not user:
#             # redirect the user to the login page
#             return HttpResponseRedirect(reverse('login')+'?next='+current_url)
#         else:
#             return f(request, *args, **kwargs)
#     return wrap

def authenticateUser(request):
    return JsonResponse(requests.post(MODELS + 'authenticate/', request.POST).json())

def search_listing(request):
    es = Elasticsearch(['es'])
    query = request.POST.get('query', None)
    results = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
    results_list = []
    for result in results['hits']['hits']:
        resp = requests.get(MODELS+ 'textbooklistings/?id='+result.get('_id')).json()
        if resp['ok']:
            results_list.append(resp['results'])
    return JsonResponse({'ok':True, 'results':results_list})
