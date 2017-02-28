import urllib.parse
import urllib.request
import json
from django.http import HttpResponse, JsonResponse


def index(request):
    #req = urllib.request.Request('http://models-api/v1/api/textbooks/')
    #resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    #resp = json.loads(resp_json)
    return JsonResponse({"results":"stuff"})
