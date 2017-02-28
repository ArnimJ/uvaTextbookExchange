from django.shortcuts import render
from .models import Textbook, TextbookPost
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.dateparse import parse_date
from django.forms.models import model_to_dict
from decimal import *
import json


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
        if id:
            try:
                results = Textbook.objects.get(id=id)
                results = forms.models.model_to_dict(results)
            except ObjectDoesNotExist:
                return JsonResponse({'results': "No textbook found"})
        else:
            results = list(Textbook.objects.values())
        return JsonResponse({'results': results})
    else:
        return JsonResponse({'results': "this is a GET method"})


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
    results = TextbookPost.objects.values_list()
    return JsonResponse({'results': list(results)})

# haven't done textbookPost POST capabilities because I'd rather have a direction to go in (ie actually implementing functionality) first
