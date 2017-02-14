from django.shortcuts import render
from marketplace.models import Textbook, TextbookPost
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django import forms


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

#go to the url, returns out all textbooks in json format
def getTextbook(request):
    results = Textbook.objects.values_list()
    return JsonResponse({'results': list(results)})

#For handling the form to add a textbook to the database
def postTextbook(request):
    if request.method =='POST':
        form = TextbookForm(request.POST)
        if form.is_valid():
            tx = Textbook.objects.create(title=form.cleaned_data['title'], isbn=form.cleaned_data['isbn'], author=form.cleaned_data['author'], publicationDate="1990-01-01", publisher="Penguin" )
        form = TextbookForm()
    #basically reload the index, with new data added
    return index(request)


#go to the url, returns out all listings in json format
def getTextbookPost(request):
    results = TextbookPost.objects.values_list()
    return JsonResponse({'results': list(results)})

#haven't done textbookPost POST capabilities because I'd rather have a direction to go in (ie actually implementing functionality) first
