from django.shortcuts import render
import urllib.parse
import urllib.request
import requests
import json
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from elasticsearch import Elasticsearch
from .forms import *
# from models.marketplace.models import Authenticator

EXP = 'http://exp-api:8000/v1/api/'

# Create your views here.
exp_endpoint = "http://exp-api:8000/v1/api/"
def index(request):
    auth_check = requests.post('http://exp-api:8000/v1/api/authenticate/', request.COOKIES).json()
    if(auth_check['ok']):
        user = auth_check['resp']
    else: user = None
    req = urllib.request.Request('http://exp-api:8000/v1/api/popularListings/')
    allposts = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    req2 = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/')
    allbooks = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))
    req1 = urllib.request.Request('http://exp-api:8000/v1/api/recentListings/')
    recentPosts = json.loads(urllib.request.urlopen(req1).read().decode('utf-8'))
    return render(request, 'index.html', {'user': user, 'postings_list': allposts['results'], 'book_list' : allbooks['results'], 'recentposts': recentPosts['results'], 'request':request})

def book_list(request):
    req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/?')
    allbooks = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    return render(request, 'book_list.html', {'book_list': allbooks['results']})

def book_detail(request, id):
    #req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/', {'id': id})
    req = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/')
    allbooks = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    book_list = allbooks['results']
    num = int(id) - 1
    b = book_list[num]
    #return render(request, 'book_detail.html', {'book_list' : allbooks['results'], 'id': id})
    return render(request, 'book_detail.html', {'book': b, 'id': id})

def login(request):
    form = LoginForm()
    text = " "
    # If we received a GET request instead of a POST request
    if request.method == 'GET':
        # display the login form page
        next = request.GET.get('next') or reverse('index')
        return render(request, 'login.html', {'form':form, 'login':True})

    # Creates a new instance of our login_form and gives it our POST data
    f = LoginForm(request.POST)


    # Check if the form instance is invalid
    if not f.is_valid():
      # Form was bad -- send them back to login page and show them an error
        return render(request, 'login.html', {'ok': False, 'error':'Incorrect form input', 'form':form})

    # Sanitize username and password fields
    username = f.cleaned_data['username']
    password = f.cleaned_data['password']

    # Get next page
    next = f.cleaned_data.get('next') or reverse('index')

    # Send validated information to our experience layer
    data = {'username':username, 'password':password}
    resp = requests.post('http://exp-api:8000/v1/api/login/', data)

    struct = {}
    try:
        dataform = str(resp).strip("'<>() ").replace('\'', '\"')
        struct = json.loads(dataform)
        text = struct["results"]
    except:
        print(repr(resp))


    # Check if the experience layer said they gave us incorrect information
    if not resp or not resp.json()['ok']:
      # Couldn't log them in, send them back to login page with error
        return render(request, 'login.html', {'form': form, 'text': text})

    """ If we made it here, we can log them in. """
    # Set their login cookie and redirect to back to wherever they came from
    resp = resp.json()
    authenticator = resp['resp']['authenticator']
    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)

    return response

def logout(request):
    if 'auth' in request.COOKIES:
        resp = requests.post('http://exp-api:8000/v1/api/logout/', request.COOKIES)
    return HttpResponseRedirect('/')

def createUser(request):
    text = " "
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'newUser.html', {'form': form, "text": text, "registered": False})

    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            resp = requests.post('http://exp-api:8000/v1/api/createUser/', form.cleaned_data)
            struct = {}
            try:
                dataform = str(resp).strip("'<>() ").replace('\'', '\"')
                struct = json.loads(dataform)
                text = struct["results"]
            except:
                print (repr(resp))
            text = resp.json()['results']
            if resp.json()['results']:
                login = requests.post('http://exp-api:8000/v1/api/login/', {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password']})
        return render(request, 'newUser.html', {'form' : form, "text":text, "registered": True})


def selling(request):
    auth_check = requests.post('http://exp-api:8000/v1/api/authenticate/', request.COOKIES).json()
    if not auth_check['ok']:
        return HttpResponseRedirect('/login/')

    user=auth_check['resp']
    if request.method == 'GET':
        form = SellingForm()
        text = " "
        return render(request, 'sell.html', {'form': form, 'text': text, 'posted': False})
    else:
        form = SellingForm(request.POST)
        if form.is_valid():
            resp = requests.post('http://exp-api:8000/v1/api/createSellPost/', form.cleaned_data)
            text = resp.json()["results"]
            # return JsonResponse(resp, safe=False)
        return render(request, 'sell.html', {'user':user, 'form': form, 'text': text, 'posted': True})

def buying(request):
    auth_check = requests.post('http://exp-api:8000/v1/api/authenticate/', request.COOKIES).json()
    if not auth_check['ok']:
        return HttpResponseRedirect('/login/')
    else:
        user = auth_check['resp']
        if request.method == 'GET':
            form = BuyingForm()
            text = " "
            return render(request, 'buy.html', {'form': form, 'text': text, 'posted': False})
        else:
            form = SellingForm(request.POST)
            if form.is_valid():
                resp = requests.post('http://exp-api:8000/v1/api/createBuyPost/', form.cleaned_data)
                text = resp.json()["results"]
                return render(request, 'buy.html', {'form': form, 'text': text, 'posted': True, 'user':user})

            # return JsonResponse(resp, safe=False)

def allListings(request):
    auth_check = requests.post('http://exp-api:8000/v1/api/authenticate/', request.COOKIES).json()
    if not auth_check['ok']:
        return HttpResponseRedirect('/login/')
    else:
        user = auth_check['resp']
        resp = requests.get('http://exp-api:8000/v1/api/allListing/')
        # allposts = resp.json()['results']
        # sellPosts = {}
        # buyPosts = {}
        # for item in allposts:
        #     if item['type'] == 'Sell':
        #         sellPosts.
    return render(request, 'alllistings.html', {'data':resp.json()['results'], 'user':user})

def listing_detail(request, id):
    auth_check = requests.post('http://exp-api:8000/v1/api/authenticate/', request.COOKIES).json()
    if not auth_check['ok']:
        return HttpResponseRedirect('/login/')
    else:
        user = auth_check['resp']
        resp = requests.post(EXP + 'listing_detail/', {'id':id}).json()
        listing = resp['listing']
        book = resp['book']
        recommendations = resp['recommendations'] #None if there are no recs for this post

        #send page view to exp to be added to log file
        resp3 = requests.post('http://exp-api:8000/v1/api/addtolog/', {'username': user['username'], 'item_id': id})

        return render(request, 'listing_detail.html', {'listing': listing, 'id': id, 'textbook': book, 'recommendations': recommendations, 'user': user})

def search_listing(request):
    if request.method == 'POST':
        auth_check = requests.post('http://exp-api:8000/v1/api/authenticate/', request.COOKIES).json()
        if(auth_check['ok']):
            user = auth_check['resp']
        else: user = None
        resp = requests.post(exp_endpoint+ 'search_listing/', request.POST).json()
        data = {'user':user}
        if resp.get('ok'):
            data['listings'] = resp.get('results')

        return render(request, 'search_results.html', data)


# def request_post(endpoint,data):
#     data_encoded = urllib.parse.urlencode(data).encode('utf-8')
#     req = urllib.request.Request(exp_endpoint + endpoint, data=data_encoded, method='POST')
#     raw = urllib.request.urlopen(req).read().decode('utf-8')
#     return json.loads(raw)








