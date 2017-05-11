import json
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.core.urlresolvers import reverse
from externaltestserver import ExternalLiveServerTestCase
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import os

class MySeleniumTests(ExternalLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Remote(
            command_executor=os.environ['SELENIUM_HOST'],
            desired_capabilities=DesiredCapabilities.CHROME
        )

    def tearDown(self):
        self.browser.quit()
        super().tearDown()


    #The following are a series of tests to test access to pages
    #Since user is not logged in they bounce user to login page
    #Test checks for this redirect


    def test_load_page(self):
        self.browser.get(self.live_server_url)
        #isPresent = self.browser.find_elements_by_id("post_table")
        #self.assertEqual(isPresent, True)
        self.assertIn("Easy to use and convenient!", self.browser.page_source)

    def test_load_login(self):
        self.browser.get(self.live_server_url+'/login')
        #isPresent = self.browser.find_elements_by_id("post_table")
        #self.assertEqual(isPresent, True)
        self.assertIn("Enter Account Information:", self.browser.page_source)

    '''
    def test_load_books(self):
        self.browser.get(self.live_server_url+'/books')
        #isPresent = self.browser.find_elements_by_id("post_table")
        #self.assertEqual(isPresent, True)
        self.assertIn("Enter Account Information:", self.browser.page_source)


    def test_load_register(self):
        self.browser.get(self.live_server_url+'/register')
        #isPresent = self.browser.find_elements_by_id("post_table")
        #self.assertEqual(isPresent, True)
        self.assertIn("Enter Account Information:", self.browser.page_source)


    def test_load_sell(self):
        self.browser.get(self.live_server_url+'/sell')
        #isPresent = self.browser.find_elements_by_id("post_table")
        #self.assertEqual(isPresent, True)
        self.assertIn("Enter Account Information:", self.browser.page_source)


    def test_load_buy(self):
        self.browser.get(self.live_server_url+'/buy')
        #isPresent = self.browser.find_elements_by_id("post_table")
        #self.assertEqual(isPresent, True)
        self.assertIn("Enter Account Information:", self.browser.page_source)


    def test_load_listings(self):
        self.browser.get(self.live_server_url+'/listings')
        #isPresent = self.browser.find_elements_by_id("post_table")
        #self.assertEqual(isPresent, True)
        self.assertIn("Enter Account Information:", self.browser.page_source)
    '''
    #checks for specific element on home page
    def test_index(self):
        self.browser.get(self.live_server_url)
        wait = ui.WebDriverWait(self.browser,10)
        isPresent = self.browser.find_elements_by_id("post_table")
        temp = []
        self.assertEqual(isPresent, temp)

