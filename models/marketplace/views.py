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
    title = forms.CharField(label='Title', max_length = 100)
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

#If an id is specified, return that textbook otherwise return all of them
def getTextbooks(request):
    if request.method == 'GET':
        id = request.GET.get('id', False)
        filter = request.GET.get('filter', False)
        results = Textbook.objects
        if id:
            try:
                results = results.get(id=id)
                results = forms.models.model_to_dict(results)
                return JsonResponse({'results': results})
            except ObjectDoesNotExist:
                return JsonResponse({'results': "No textbook found"})
        elif filter:
            results = results.filter(filter)
        else:
            results = list(Textbook.objects.values())
        return JsonResponse({'results': results})
    else: return JsonResponse({'results': "this is a GET method, you gave " + request.method})

#Delete the textbook as specified by id
def deleteTextbook(request):
    if request.method == 'POST':
        id = request.POST.get('id', False)
        if id:
            try:
                results = Textbook.objects.get(id=id).delete()
                return JsonResponse({'results':"Success"})
            except ObjectDoesNotExist:
                return JsonResponse({'results':"No textbook found"})
        else:
            return JsonResponse({'results':"No ID specified"})
    else: return JsonResponse({'results':"This is a POST method"})


#For handling the form to add a textbook to the database
def postTextbookByForm(request):
    if request.method =='POST':
        form = TextbookForm(request.POST)
        if form.is_valid():
            tx = Textbook.objects.create(title=form.cleaned_data['title'], isbn=form.cleaned_data['isbn'], author=form.cleaned_data['author'], publicationDate="1990-01-01", publisher="Penguin" )
        form = TextbookForm()
    #basically reload the index, with new data added
    return index(request)


def createTextbook(request):
    if request.method == 'POST':
        try:
            title1 = request.POST.get('title')
            isbn1 = request.POST.get('isbn')
            author1 = request.POST.get('author')
            publicationDate1 = request.POST.get('pubdate')
            publisher1 = request.POST.get('publisher')

            Textbook.objects.create(title=request.POST.get('title'), isbn=request.POST.get('isbn'), author=request.POST.get('author'), publicationDate=request.POST.get('pubdate'), publisher=request.POST.get('publisher'))
            return JsonResponse({'results':'Success'})
        except IntegrityError:
            return JsonResponse({'results':'You need both the title and author to create an entry or your isbn field might be incorrect'})


#for updating an exisiting textbook
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
                    if type(newIsbn) is int:
                        object.isbn=newIsbn
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
        else:
            return JsonResponse({'results': "No ID specified"})
    else: return JsonResponse({'results': "This is a POST method"})


#update an existing textbookPost
def updateTextbook(request):
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
                    if newSold == "True" or newSold == "true"  or newSold == "False" or newSold == "false":
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



#go to the url, returns out all listings in json format
def getTextbookPost(request):
    results = TextbookPost.objects.values_list()
    return JsonResponse({'results': list(results)})

#we want to avoid model-level apis this specific in order to reduce clutter on the model
#level. The solution is basically make our get apis advanced enough that enough filtering
#and such parameters can be passed through that we can accomplish this through a more basic
#getPost method
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
