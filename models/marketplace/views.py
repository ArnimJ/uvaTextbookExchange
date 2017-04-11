from django.shortcuts import render
from .models import Textbook, TextbookPost, User, Authenticator
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.dateparse import parse_date
from django.forms.models import model_to_dict
from decimal import *
# from django.urls import reverse
from django.contrib.auth import hashers
# from web.frontend.forms import *
from datetime import datetime, timedelta
from django.utils import timezone
import hmac
import models.settings as settings
import os
from django.core import serializers


class TextbookForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    isbn = forms.IntegerField(label='ISBN')
    author = forms.CharField(label='Author')


# Create your views here.
def index(request):
    query_results = Textbook.objects.all()
    template = loader.get_template('index.html')
    form = TextbookForm()
    context = {
        'query_results': query_results,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


# If an id is specified, return that textbook otherwise return all of them
def getTextbooks(request):
    if request.method == 'GET':
        id = request.GET.get('id', False)
        filter = request.GET.get('filter', False)
        results = Textbook.objects
        if id:
            try:
                results = results.get(id=id)
                results = forms.models.model_to_dict(results)
                return JsonResponse({'ok':True, 'results': results})
            except ObjectDoesNotExist:
                return JsonResponse({'ok':False,'results': "No textbook found"})
        elif filter:
            results = results.filter(filter)
        else:
            results = list(Textbook.objects.values())
        return JsonResponse({'results': results})

    else:
        return JsonResponse({'ok':False,'results': "this is a GET method, you gave " + request.method})


# Delete the textbook as specified by id
def deleteTextbook(request):
    if request.method == 'POST':
        id = request.POST.get('id', False)
        if id:
            try:
                results = Textbook.objects.get(id=id).delete()
                return JsonResponse({'results': "Success"})
            except ObjectDoesNotExist:
                return JsonResponse({'results': "No textbook found"})
        else:
            return JsonResponse({'results': "No ID specified"})
    else:
        return JsonResponse({'results': "This is a POST method"})


# For handling the form to add a textbook to the database
def postTextbookByForm(request):
    if request.method == 'POST':
        form = TextbookForm(request.POST)
        if form.is_valid():
            tx = Textbook.objects.create(title=form.cleaned_data['title'], isbn=form.cleaned_data['isbn'],
                                         author=form.cleaned_data['author'], publicationDate="1990-01-01",
                                         publisher="Penguin")
        form = TextbookForm()
    # basically reload the index, with new data added
    return index(request)


def createTextbook(request):
    if request.method == 'POST':
        try:
            title1 = request.POST.get('title', False)
            if not title1:
                return JsonResponse({'results': 'You need a title'})

            isbn1 = request.POST.get('isbn', False)
            if not isbn1 or type(isbn1) is Decimal:
                return JsonResponse({'results': 'You need a isbn'})

            author1 = request.POST.get('author', False)
            if not author1:
                return JsonResponse({'results': 'You need a author'})

            # TODO: need to figure out how to parse date

            Textbook.objects.create(title=request.POST.get('title'), isbn=request.POST.get('isbn'),
                                    author=request.POST.get('author'), publicationDate=request.POST.get('pubdate'),
                                    publisher=request.POST.get('publisher'))
            return JsonResponse({'results': 'Success'})
        except IntegrityError:
            return JsonResponse({'results': 'something went very wrong'})
        except ValueError:
            return JsonResponse(
                {'results': 'you tried to put a string for a isbn'})
    else:
        return JsonResponse({'results': "This is a POST method"})


# for updating an exisiting textbook
def updateTextbook(request):
    if request.method == 'POST':
        id = request.POST.get('id', False)
        newTitle = request.POST.get('title', False)
        newIsbn = request.POST.get('isbn', False)
        newAuthor = request.POST.get('author', False)
        newPublicationsDate = request.POST.get('publicationDate', False)
        newPublisher = request.POST.get('publisher', False)
        if id:
            try:
                object = Textbook.objects.get(id=id)
                if newTitle:
                    object.title = newTitle
                if newIsbn:
                    object.isbn = int(newIsbn)
                if newAuthor:
                    object.author = newAuthor
                if newPublicationsDate:
                    date = parse_date(newPublicationsDate)
                    object.newPublicationsDate = date
                if newPublisher:
                    object.publisher = newPublisher
                object.save()
                returnObject = model_to_dict(object)
                return JsonResponse({'results': returnObject})
            except ObjectDoesNotExist:
                return JsonResponse({'results': "No textbook found"})
            except ValueError:
                return JsonResponse(
                    {'results': 'you tried to put a string for a isbn'})
        else:
            return JsonResponse({'results': "No ID specified"})
    else:
        return JsonResponse({'results': "This is a POST method"})


# update an existing textbookPost
def updateTextbookPost(request):
    if request.method == 'POST':
        id = request.POST.get('id', False)
        newPostTitle = request.POST.get('postTitle', False)
        newCondition = request.POST.get('condition', False)
        newPrice = request.POST.get('price', False)
        newCatagory = request.POST.get('category', False)
        newSold = request.POST.get('sold', False)
        if id:
            try:
                object = TextbookPost.objects.get(id=id)
                if newPostTitle:
                    object.postTitle = newPostTitle
                if newCondition:
                    object.condition = newCondition
                if newPrice:
                    if type(newPrice) is Decimal:
                        object.price = newPrice
                if newCatagory:
                    object.catagory = newCatagory
                if newSold:
                    if newSold == "True" or newSold == "true" or newSold == "False" or newSold == "false":
                        object.sold = newSold
                object.save()
                returnObject = model_to_dict(object)
                return JsonResponse({'results': returnObject})
            except ObjectDoesNotExist:
                return JsonResponse({'results': "No textbook found"})
        else:
            return JsonResponse({'results': "No ID specified"})
    else:
        return JsonResponse({'results': "This is a POST method"})


# go to the url, returns out all listings in json format
def getTextbookPost(request):
    if request.method == 'GET':
        id = request.GET.get('id', False)
        filter = request.GET.get('filter', False)
        results = TextbookPost.objects
        if id:
            try:
                results = results.get(id=id)
                results = forms.models.model_to_dict(results)
                return JsonResponse({'ok':True, 'results': results})
            except ObjectDoesNotExist:
                return JsonResponse({'ok':False,'results': "No listing found with that ID"})
        elif filter:
            results = results.filter(filter)
        else:
            results = list(TextbookPost.objects.values())
        return JsonResponse({'ok':True,'results': results})
    else:
        return JsonResponse({'ok':False,'results': "this is a GET method, you gave " + request.method})


def getPopularPosts(request):
    if request.method == 'GET':
        pop = TextbookPost.objects.filter(sold=False).order_by('-viewCount')[:4].values()
        return JsonResponse({'results': list(pop)})
    else:
        return JsonResponse({'results': "This is a GET method"})


def getRecentPosts(request):
    if request.method == 'GET':
        rec = TextbookPost.objects.filter(sold=False).order_by('-postDate')[:4].values()
        return JsonResponse({'results': list(rec)})
    else:
        return JsonResponse({'results': "This is a GET method"})


def getUser(request):
 if request.method == 'GET':
        username = request.GET.get('username', False)
        id = request.GET.get('id', False)
        filter = request.GET.get('filter', False)
        results = User.objects
        if id:
            try:
                results = results.get(id=id)
                results = forms.models.model_to_dict(results)
                return JsonResponse({'results': results})
            except ObjectDoesNotExist:
                return JsonResponse({'results': "No user found with that ID"})
        elif username:
            try:
                results = results.get(id=id)
                results = forms.models.model_to_dict(results)
                return JsonResponse({'results': results})
            except ObjectDoesNotExist:
                return JsonResponse({'results': "No user found with that username"})
        elif filter:
            results = results.filter(filter)
        else:
            results = list(User.objects.values())
        return JsonResponse({'results': results})
 else:
     return JsonResponse({'results': "this is a GET method, you gave " + request.method})


def createUser(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username', False)
            if not username:
                return JsonResponse({'results': 'You need a username'})

            password = request.POST.get('password', False)
            if not password:
                return JsonResponse({'results': 'You need a password'})

            email = request.POST.get('email', False)
            if not email:
                return JsonResponse({'results': 'You need an email'})

            try:
                User.objects.get(username=request.POST.get('username'))
                return JsonResponse({'results': 'That username is already taken'})
            except User.DoesNotExist:
                pass


            passhash = hashers.make_password(password)

            User(username=username, passhash=passhash,
                                    email=email).save()

            return JsonResponse({'results': 'Success'})

        except IntegrityError:
            return JsonResponse({'results': 'something went very wrong'})
        except ValueError:
            return JsonResponse({'results': 'You got a ValueError'})
    else:
        return JsonResponse({'results': "This is a POST method"})

def authenticateUser(request):
    if request.method == 'POST':
        try:  # tests if the user has an authenticator that matches the one the database has for them and is not expired
            auth = Authenticator.objects.get(authenticator=request.POST.get('auth'))
            if (auth.date_created > timezone.now() - timedelta(days=1)):
                return _success_response(request)
        except Authenticator.DoesNotExist:
            pass
        return _error_response(request, 'failure')


def logout(request):
    try:
        Authenticator.objects.get(authenticator=request.POST['auth']).delete()
        return _success_response(request, 'User logged out successfully')
    except:
        return _error_response(request, 'That user is not logged in')


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return _error_response(request, 'That user does not exist')

    if not hashers.check_password(password, user.passhash):
        return _error_response(request, 'Incorrect password')

    while (True):
        authenticator = hmac.new(
            key=settings.SECRET_KEY.encode('utf-8'),
            msg=os.urandom(32),
            digestmod='sha256',
        ).hexdigest()
        try:
            Authenticator.objects.get(authenticator=authenticator)
        except Authenticator.DoesNotExist:
            break

    try:
        Authenticator.objects.get(user_id=user).delete()
        auth = Authenticator.objects.create(user_id=user, authenticator=authenticator)
    except:
        auth = Authenticator.objects.create(user_id=user, authenticator=authenticator)

    auth.save()
    auth = model_to_dict(auth)
    return _success_response(request, auth)


def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})


def _success_response(request, resp=None):
    if resp:
        return JsonResponse({'ok': True, 'resp': resp})
    else:
        return JsonResponse({'ok': True})


def createBuyPost(request):
        if request.method == 'POST':
            try:

                postTextbookName = request.POST.get('textbookName', "")
                postTextbookISBN = request.POST.get('isbn', "")
                postTextbookAuthor = request.POST.get('author', "")

                if postTextbookName == "" or postTextbookAuthor == "":
                    return JsonResponse({
                        "results": "Something was not passed in textbook."
                    })



                postTitle = request.POST.get('title', "")
                postPrice = request.POST.get('price', False)
                postCondition = request.POST.get('condition', False)
                postDetail = request.POST.get('details', None)

                if postTitle == "":
                    return JsonResponse({
                        "results": "Something was not passed in posttitle."
                    })

                if postPrice == False:
                    return JsonResponse({
                        "results": "Something was not passed in price."
                    })

                if postCondition == False:
                    return JsonResponse({
                        "results": "Something was not passed in condition."
                    })

                if postDetail == "":
                    return JsonResponse({
                        "results": "Something was not passed in detail."
                    })

                textbook = Textbook(
                    title=postTextbookName,
                    isbn=postTextbookISBN, #TODO: if textbook's isbn number already is in database, do not add
                    author=postTextbookAuthor
                )
                textbook.save()

                post = TextbookPost(
                    postTitle=postTitle,
                    textbook=textbook,
                    condition=postCondition,
                    price=postPrice,
                    details=postDetail,
                    sold=False,
                    type="Buy"
                )
                post.save()

                return JsonResponse({'results': 'Success'})

            except IntegrityError:
                return JsonResponse({'results': 'something went very wrong'})
            except ValueError:
                return JsonResponse({'results': 'You got a ValueError'})
        else:
            return JsonResponse({'results': "This is a POST method"})


def createSellPost(request):
    if request.method == 'POST':
        try:
            postTextbookName = request.POST.get('textbookName', "")
            postTextbookISBN = request.POST.get('isbn', "")
            postTextbookAuthor = request.POST.get('author', "")

            if postTextbookName =="" or postTextbookAuthor=="":
                return JsonResponse({
                    "results": "Something was not passed in textbook."
                })

            postTitle = request.POST.get('title', "")
            postPrice = request.POST.get('price', False)
            postCondition = request.POST.get('condition', False)
            postDetail = request.POST.get('details', None)

            if postTitle == "":
                return JsonResponse({
                    "results": "Something was not passed in posttitle."
                })

            if postPrice == False:
                return JsonResponse({
                    "results": "Something was not passed in price."
                })

            if postCondition == False:
                return JsonResponse({
                    "results": "Something was not passed in condition."
                })

            if postDetail == "":
                return JsonResponse({
                    "results": "Something was not passed in detail."
                })


            textbook = Textbook(
                title=postTextbookName,
                isbn=postTextbookISBN,
                author=postTextbookAuthor
            )
            textbook.save()

            post = TextbookPost(
                postTitle=postTitle,
                textbook=textbook,
                condition=postCondition,
                price=postPrice,
                details=postDetail,
                sold=False,
                type="Sell"
            )
            post.save()
            obj = TextbookPost.objects.get(pk=post.pk)
            return_object = model_to_dict(obj)
            return JsonResponse({'results': 'Success', 'data':return_object})

        except IntegrityError:
            return JsonResponse({'results': 'something went very wrong'})
        except ValueError:
            return JsonResponse({'results': 'You got a ValueError'})
    else:
        return JsonResponse({'results': "This is a POST method"})





# haven't done textbookPost POST capabilities because I'd rather have a direction to go in (ie actually implementing functionality) first

# we want to avoid model-level apis this specific in order to reduce clutter on the model
# level. The solution is basically make our get apis advanced enough that enough filtering
# and such parameters can be passed through that we can accomplish this through a more basic
# getPost method
