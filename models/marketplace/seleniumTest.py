from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ["db.json"]

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_index(self):
        self.selenium.get(self.live_server_url)
        isPresent = self.selenium.find_elements_by_id("post_table")
        self.assertEqual(isPresent, True)

    def test_login(self):
        self.selenium.get(self.live_server_url, 'login')
        isPresent = self.selenium.find_elements_by_id("submit")
        self.assertEqual(isPresent, True)

    def test_invalid_login(self):
        self.selenium.get(self.live_server_url, 'login')
        response = self.selenium.find_elements_by_id("submit").click()
        self.assertEqual(response, (self.live_server_url+'login'))

    def test_create_book(self):
        book = Textbook.objects.create(title="Cool Book",isbn="9781118324561",author="Jerome Hicks",publicationDate="2014-01-01",publisher="Penguin")
        book.refresh_from_db()
        self.assertEqual(book.title, 'changed name')

    def test_create_post(self):
        post = TextbookPost.objects.create(postTitle="this_post", textbook="test book", condition="new", price="25.00", category="Science", details="try it out", postDate="2014-01-01")
        post.refresh_from_db()
        self.assertEqual(post.title, 'changed name')

    def test_create_user(self):
        user = User.objects.create(username="hi", passhash="hash", email="freemail@gmail.com")
        user.refresh_from_db()
        self.assertEqual(user.title, 'changed name')

    def test_static_files(self):
        self.selenium.get(self.live_server_url)
        isPresent = self.selenium.find_elements_by_id("static_image")
        self.assertEqual(isPresent, True)
