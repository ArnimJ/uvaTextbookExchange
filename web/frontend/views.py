from django.shortcuts import render
import urllib.parse
import urllib.request
import requests
import json
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse

from .forms import *
# from models.marketplace.models import Authenticator

# Create your views here.
exp_endpoint = "http://exp-api:8000/v1/api/"
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
    req2 = urllib.request.Request('http://exp-api:8000/v1/api/textbooks/')
    allbooks = json.loads(urllib.request.urlopen(req2).read().decode('utf-8'))
    req1 = urllib.request.Request('http://exp-api:8000/v1/api/recentListings/')
    recentPosts = json.loads(urllib.request.urlopen(req1).read().decode('utf-8'))
    return render(request, 'index.html', {'postings_list': allposts['results'], 'book_list' : allbooks['results'], 'recentposts': recentPosts['results']})

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
    # If we received a GET request instead of a POST request
    if request.method == 'GET':
        # display the login form page
        next = request.GET.get('next') or reverse('index')
        return render(request, 'login.html', {'form':form})

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
    next = f.cleaned_data.get('next') or reverse('home')

    # Send validated information to our experience layer
    data = {'username':username, 'password':password}
    resp = requests.post('http://exp-api:8000/v1/api/login', data)
    resp = json.loads(resp.text)

    # Check if the experience layer said they gave us incorrect information
    if not resp or not resp['ok']:
      # Couldn't log them in, send them back to login page with error
        resp.put('form', form)
        return render(request, 'login.html', {'form': form})

    """ If we made it here, we can log them in. """
    # Set their login cookie and redirect to back to wherever they came from
    authenticator = resp['authenticator']

    response = HttpResponseRedirect(next)
    response.set_cookie("auth", authenticator)

    return response

def createUser(request):
    if request.method == 'GET':
        form = SignupForm()
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            resp = requests.post('http://exp-api:8000/v1/api/createUser', form.cleaned_data)
            return HttpResponseRedirect(reverse('index'), resp)
    return render(request, 'register.html', {'form' : form})


def selling(request):
    if request.method == 'GET':
        form = SellingForm()
        text = " "
    else:
        form = SellingForm(request.POST)
        if form.is_valid():
            resp = requests.post('http://exp-api:8000/v1/api/createSellPost/', form.cleaned_data)
            text = resp.json()["results"]

            # return JsonResponse(resp, safe=False)
    return render(request, 'sell.html', {'form': form, 'text': text})

def buying(request):
    if request.method == 'GET':
        form = BuyingForm()
    else:
        form = BuyingForm(request.POST)
        if form.is_valid():
            resp = requests.post('http://exp-api:8000/v1/api/createBuyPost/', form.cleaned_data)
    return render(request, 'buy.html', {'form': form})

def register(request):
    return render(request, 'register.html')



# def request_post(endpoint,data):
#     data_encoded = urllib.parse.urlencode(data).encode('utf-8')
#     req = urllib.request.Request(exp_endpoint + endpoint, data=data_encoded, method='POST')
#     raw = urllib.request.urlopen(req).read().decode('utf-8')
#     return json.loads(raw)








    