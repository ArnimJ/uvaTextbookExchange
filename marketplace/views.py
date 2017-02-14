from django.shortcuts import render
from marketplace.models import Textbook, TextbookPost
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'index.html', context = None)

def getTextbook(request):
	return HttpResponse(Textbook.objects.all())