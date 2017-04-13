from django.forms.models import model_to_dict
import requests
from elasticsearch import Elasticsearch

MODELS = 'http://models-api:8000/v1/api/'

while(True):
    resp = requests.get(MODELS + 'textbooklistings/').json()
    list = []
    if len(resp) > 0:
        while(True):
            try:
                es = Elasticsearch(['es'])
                break
            except:
                pass
        for listing in resp['results']:
            dict = listing#(model_to_dict(listing))
            dict['textbook'] = requests.get(MODELS + 'textbooks/?id='+repr(dict['textbook_id'])).json().get('results')
            list.append(dict)
        for listing in list:
            while(True):
                try:
                    es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
                    break
                except:
                    pass
        es.indices.refresh(index='listing_index')
        break
