from django.shortcuts import render
from marketplace.models import Textbook, TextbookPost
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
	query_results = Textbook.objects.all()
	template = loader.get_template('index.html')
	context = {
	    'query_results': query_results,
	}
	return HttpResponse(template.render(context, request))

def getTextbook(request):
	return HttpResponse(Textbook.objects.all())