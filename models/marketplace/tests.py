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


# Create your tests here.
class textbookTests(TestCase):
    fixtures = ["db.json"]

    def success_response(self):
        # assumes user with id 1 is stored in db
        response = self.client.get(reverse('getTextbooks', kwargs={'user_id': 1}))

        # checks that response contains parameter id & implicitly
        # checks that the HTTP status code is 200
        self.assertContains(response, 'id')

    # user_id not given in url, so error
    def fails_invalid(self):
        response = self.client.get(reverse(''))
        self.assertEquals(response.status_code, 404)
