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
#from models import TextbookPost, Textbook, User
import json
import codecs


# Create your tests here.

class GetTextbookTestCases(TestCase):

    fixtures = ["db.json"]
    # setUp method is called before each test in this class
    def setUp(self):
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

    def test_Post(self): #make sure only 'get' methods work
        response = self.client.post(reverse('allTextbooks'))
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "this is a GET method, you gave POST")

    def test_Incorrect_Id(self): #if invalid id is passed, should a message
        response = self.client.get(reverse('allTextbooks'), {'id': 1000})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "No textbook found")

    # tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down


class DeleteTextbookTestCases (TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        pass

    def test_success_response(self): #same as above
        response = self.client.post(reverse('deleteBook'), {'id': 1})
        self.assertContains(response, 'Success')

    def test_no_ID_Given(self): #no id given test case
        response = self.client.post(reverse('deleteBook'))
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "No ID specified")

    def test_id_Given(self): #valid id given test case
        response = self.client.post(reverse('deleteBook'), {'id': 1})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Success')

    def test_Incorrect_Id(self):  # if invalid id is passed, should a message
        response = self.client.post(reverse('deleteBook'), {'id': 1000})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'No textbook found')

    def test_Get(self): #should check for get methods
        response = self.client.get(reverse('deleteBook'))
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "This is a POST method")

    #tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

class CreateTextbookTestCases(TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        pass

    def test_success_response(self): #same as above
        response = self.client.post(reverse('createTextbook'), {'title': 'test' , 'isbn': 123456789013, 'author': 'james'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Success')

    def test_Creation(self): #if all parameters are given, test if response is success
        response = self.client.post(reverse('createTextbook'), {'title': 'test' , 'isbn': 123456789013, 'author': 'james'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Success')

    def test_No_author_given(self): #test case when author is not given
        response = self.client.post(reverse('createTextbook'), {'title': 'test', 'isbn': 123456789013})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'You need a author')

    def test_No_Title_Given(self): #test case when title is not given
        response = self.client.post(reverse('createTextbook'), {'isbn': 123456789013, 'author': 'james'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'You need a title')

    def test_No_Isbn_Given(self): #test case when isbn is not given
        response = self.client.post(reverse('createTextbook'), {'title': 'test' , 'author': 'james'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'You need a isbn')

    def test_Incorrect_type(self): #test for when user inputs non numeral type into a isbn field
        response = self.client.post(reverse('createTextbook'), {'title': 'testing', 'isbn': 'jack', 'author': 'james'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'you tried to put a string for a isbn')

    def test_Get(self): #should check for get methods
        response = self.client.get(reverse('createTextbook'), {'title': 'test' , 'isbn': 123456789013, 'author': 'james'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "This is a POST method")

    #tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

class UpdateTextbookTextcases(TestCase):
    fixtures = ["db.json"]
    def setUp(self):
        pass

    def test_success_response(self):  # same as above
        response = self.client.post(reverse('updateTextbook'), {'id':1 , 'title': 'newTitle'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        print(value['id'])
        self.assertEquals(value['id'], 1)

    def test_update_title(self): ##updating just one field works
        response = self.client.post(reverse('updateTextbook'), {'id':1 , 'title': 'newTitle'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value['title'],'newTitle')

    def test_update_multiple_fields(self): #updating multiple fields
        response = self.client.post(reverse('updateTextbook'), {'id':1 , 'title': 'newTitle', 'isbn': 123456878, 'author': 'testing'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value['title'], 'newTitle')
        self.assertEquals(value['isbn'], 123456878)
        self.assertEquals(value['author'], 'testing')

    def test_Incorrect_type(self): #string for isbn should produce certain response
        response = self.client.post(reverse('updateTextbook'), {'id':1 , 'isbn': 'newTitle'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'you tried to put a string for a isbn')

    def no_id_given(self): #test case for when no id is given
        response = self.client.post(reverse('updateTextbook'), {'title': 'newTitle'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "No ID specified")

    def test_Get(self): #should check for get methods
        response = self.client.get(reverse('updateTextbook'), {'id':1 , 'isbn': 'newTitle'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "This is a POST method")

    #tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

class GetTextbookPostTestCase(TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        pass

    def test_success_response(self):  # tests both response and if getting textbook by id works
        response = self.client.get(reverse('getTextbookPosts'), {'id': 1})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value['id'],1)

    def test_noPramsGiven(self): #no id should return all textbooksposts in db
        response = self.client.get(reverse('getTextbookPosts'))
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        id_list = []
        count = 0
        for i in value:
            count = count +1
        self.assertGreaterEqual(count,1)

    def test_method_type(self): #make sure it is a get request
        response = self.client.post(reverse('getTextbookPosts'), {'id': 1})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, "this is a GET method, you gave POST")

class GetPopularPostsTestCases(TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        pass

    def test_success_response(self):  # tests both response and api is working
        response = self.client.get(reverse('getPopularPosts'))
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        count = 0
        for i in value:
            count = count +1

        self.assertGreaterEqual(count, 1)

    #Later when the postings actually have views, i will write a unit test to confirm they are in the right order
    #tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

class TestGetRecentPosts(TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        pass

    def test_success_response(self):  # tests both response and api is working
        response = self.client.get(reverse('getRecentPosts'))
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        count = 0
        for i in value:
            count = count +1

        self.assertGreaterEqual(count, 1)

    #Later when the postings actually have views, i will write a unit test to confirm they are in the right order

    #tearDown method is called after each test
    def tearDown(self):
        pass  # nothing to tear down

#NEW TESTS START HERE
class TestCreateSellPost(TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        pass

    def test_success_response(self): #test a successful post
        response = self.client.post(reverse('createSell'), {'textbookName': 'test', 'isbn': 123456789013, 'author': 'me', 'title': 'posttitle', 'price': 3, 'condition': 'Good', 'details': 'blah'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Success')

    def test_no_textbook_title_given(self): #test case only textbook title isn't given
        response = self.client.post(reverse('createSell'), {'isbn': 123456789013, 'author': 'me', 'title': 'posttitle', 'price': 3, 'condition': 'Good', 'details': 'blah'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Something was not passed in textbook.')

    def test_no_author_given(self): #test case only author isn't given
        response = self.client.post(reverse('createSell'), {'textbookName': 'test', 'isbn': 123456789013, 'title': 'posttitle', 'price': 3, 'condition': 'Good', 'details': 'blah'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Something was not passed in textbook.')

    def test_no_post_title_given(self): #test case only posttitle isn't given
        response = self.client.post(reverse('createSell'), {'textbookName': 'test', 'isbn': 123456789013, 'author': 'me', 'price': 3, 'condition': 'Good', 'details': 'blah'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Something was not passed in posttitle.')

    def test_no_post_price_given(self): #test case only posttitle isn't given
        response = self.client.post(reverse('createSell'), {'textbookName': 'test', 'isbn': 123456789013, 'author': 'me', 'title': 'posttitle', 'condition': 'Good', 'details': 'blah'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Something was not passed in price.')

    def test_no_post_condition_response(self): #test a post with no condition
        response = self.client.post(reverse('createSell'), {'textbookName': 'test', 'isbn': 123456789013, 'author': 'me', 'title': 'posttitle', 'price': 3, 'details': 'blah'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Something was not passed in condition.')

    def test_no_post_detail_response(self): #test a post with no detail
        response = self.client.post(reverse('createSell'), {'textbookName': 'test', 'isbn': 123456789013, 'author': 'me', 'title': 'posttitle', 'price': 3, 'condition': 'Good'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'something went very wrong')

class TestCreateUser(TestCase):
    fixtures = ["db.json"]

    def setUp(self):
        pass

    def test_success_response(self): #test a successful post
        response = self.client.post(reverse('createUser'), {'username': 'apple', 'password': 'secret', 'email': 'me@gmail.com'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'Success')

    def test_no_username_response(self): #test post with no username
        response = self.client.post(reverse('createUser'), {'password': 'secret', 'email': 'me@gmail.com'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'You need a username')

    def test_no_password_response(self): #test a post with no password
        response = self.client.post(reverse('createUser'), {'username': 'apple', 'email': 'me@gmail.com'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'You need a password')

    def test_no_email_response(self): #test a post with no email
        response = self.client.post(reverse('createUser'), {'username': 'apple', 'password': 'secret'})
        response_dict = json.loads(response.content.decode('utf-8'))
        value = response_dict['results']
        self.assertEquals(value, 'You need an email')



