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
        if id:
            results = Textbook.objects.get(id=id)
            results = forms.models.model_to_dict(results)
        else:
            results = list(Textbook.objects.values_list())
        return JsonResponse({'results': results})
    else: return JsonResponse({'results': "this is a GET method"})

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
            Textbook.objects.create(title=request.POST.get('title'), isbn=request.POST.get('isbn'), author=request.POST.get('author'), publicationDate=request.POST.get('pubdate'), publisher=request.POST.get('publisher'))
            return JsonResponse({'results':'Success'})
        except IntegrityError:
            return JsonResponse({'results':'You need both the title and author to create an entry or your isbn field might be incorrect'})


#for updating an exisiting textbook
def updateTextbook(request):
    if request.method == 'POST':
        id = request.Post.get('id', False)
        newTitle = request.Post.get('title', False)
        newIsbn = request.Post.get('isbn', False)
        newAuthor = request.Post.get('author', False)
        newPublicationsDate = request.Post.get('publicationDate', False)
        newPublisher = request.Post.get('publisher', False)
        if id:
            try:
                object = Textbook.objects.get(id=id)
                if newTitle:
                    object.update(title = newTitle)
                if newIsbn:
                    if type(newIsbn) is int:
                        object.update(isbn=newIsbn)
                if newAuthor:
                    object.update(author = newAuthor)
                if newPublicationsDate:
                    date = parse_date(newPublicationsDate)
                    object.update(newPublicationsDate = date)
                if newPublisher:
                    object.update(publisher = newPublisher)
                returnObject = model_to_dict(object)
                return JsonResponse({'results': returnObject})
            except ObjectDoesNotExist:
                return JsonResponse({'results': "No textbook found"})
        else:
            return JsonResponse({'results': "No ID specified"})
    else: return JsonResponse({'results': "This is a POST method"})



#go to the url, returns out all listings in json format
def getTextbookPost(request):
    results = TextbookPost.objects.values_list()
    return JsonResponse({'results': list(results)})

#haven't done textbookPost POST capabilities because I'd rather have a direction to go in (ie actually implementing functionality) first
