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

def register(request):
    return render(request, 'register.html')

    # name_pattern = re.compile("^(([a-zA-Z]+-*)*[a-zA-Z]+)+$")
    # first_name = request.POST.get('first_name', '')
    # last_name = request.POST.get('last_name', '')
    #
    # if not name_pattern.match(first_name):
    #     return render(request, 'register.html', {'message': 'That is not a valid first name.'})
    # elif not name_pattern.match(last_name):
    #     return render(request, 'register.html', {'message': 'That is not a valid last name.'})
    #
    # email_pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    # email = request.POST.get('email', '')
    # if not email_pattern.match(email):
    #     return render(request, 'register.html', {'message': 'That is not a valid email address.'})
    #
    # username_pattern = re.compile("(?=^.{3,20}$)^[a-zA-Z][a-zA-Z0-9]*[._-]?[a-zA-Z0-9]+$")
    # username = request.POST.get('username', '')
    # if not username_pattern.match(username):
    #     return render(request, 'register.html', {'message': 'That is not a valid username.'})
    #
    # password = request.POST.get('password', '')
    # try:
    #     validate_password(password, settings.AUTH_PASSWORD_VALIDATORS)
    # except ValidationError as e:
    #     return render(request, 'register.html', {
    #         'validations': e
    #     })
    #
    # address = request.POST.get('address', '')
    # if not address:
    #     return render(request, 'register.html', {'message': 'That is not a valid address'})
    #
    # city = request.POST.get('city', '')
    # if not city:
    #     return render(request, 'register.html', {'message': 'That is not a valid city.'})
    #
    # state = request.POST.get('state', '')
    # if not state:
    #     return render(request, 'register.html', {'message': 'That is not a valid state.'})
    #
    # zipcode_pattern = re.compile("^[0-9]{4,7}$")
    # zipcode = request.POST.get('zipcode', '')
    # if not zipcode_pattern.match(zipcode):
    #     return render(request, 'register.html', {'message': 'That is not a valid zipcode.'})

    # try:
    #     user = User.objects.get(username=username)
    #     return render(request, 'register.html', {'message': 'That username is already in use.'})
    # except:
    #     pass