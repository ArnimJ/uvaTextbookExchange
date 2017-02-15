from django.shortcuts import render
from marketplace.models import Textbook, TextbookPost
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


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
            return JsonResponse({'results':'You need both the title and author to create an entry'})



#go to the url, returns out all listings in json format
def getTextbookPost(request):
    results = TextbookPost.objects.values_list()
    return JsonResponse({'results': list(results)})

#haven't done textbookPost POST capabilities because I'd rather have a direction to go in (ie actually implementing functionality) first
