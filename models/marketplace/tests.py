from django.test import TestCase
from django.conf.urls import include, url
from django.contrib import admin
from .models import Textbook, TextbookPost
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.dateparse import parse_date
from django.forms.models import model_to_dict
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import json
import codecs

# Create your tests here.
class TextbookTestCase(TestCase):
    fixtures = ["db.json"]
    # setUp method is called before each test in this class
    def setUp(self):
        #Textbook.objects.create(id=1, title = "testing", isbn = "1234567898761")
        pass

    def test_success_response(self):
        # assumes user with id 1 is stored in db
        response = self.client.get(reverse('allTextbooks'), {'id': 1})
        # checks that response contains parameter id & implicitly
        # checks that the HTTP status code is 200
        self.assertContains(response, 'id')

    def test_no_ID_Given(self):
        response = self.client.get(reverse('allTextbooks'))
        #check that there are three textbooks in the response
        response_dict = json.loads(response.content.decode('utf-8'))
        id_list = []
        value = response_dict['results']

        for i in value:
            id_list.append(i['id'])

        self.assertEquals(len(id_list), 3)

    def test_id_Given(self): #passing in an  valid id yields correct results
        response = self.client.get(reverse('allTextbooks'), {'id': 1})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value['id'],1)

    def test_Post(self): #make sure only get methods work
        response = self.client.post(reverse('allTextbooks'))
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "this is a GET method")

    def test_Incorrect_Id(self): #if invalid id is passed, should a message
        response = self.client.get(reverse('allTextbooks'), {'id': 1000})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "No textbook found")

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down


