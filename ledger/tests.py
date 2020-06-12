from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class SearchTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        # driver = webdriver.Chrome('./chromedriver')
        self.selenium.get('http://localhost:8000/')
        super(SearchTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(SearchTestCase, self).tearDown()

    def test_search_query_enter(self):
        selenium = self.selenium
        search_input = selenium.find_element_by_id('autocomplete')
        search_input.send_keys('stran', Keys.ARROW_DOWN)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)# wait for page to load

        self.assertEqual(selenium.current_url[-1], "1")

    def test_search_query_click(self):
        selenium = self.selenium
        search_input = selenium.find_element_by_id('autocomplete')
        search_input.send_keys('n')
        breakpoint()
        a = selenium.find_element_by_id('ulist').find_elements_by_class_name('active')[0]
        time.sleep(2) # wait for page to load

        self.assertEqual(selenium.current_url[-1], "1")