import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase

import unittest

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

GECKODRIVER_BIN = os.path.join( PARENT_DIR, 'bin' )
os.environ["PATH"]+=":"+GECKODRIVER_BIN

FIREFOX_PATH = "/usr/local/firefox/firefox"

def build_browser():
    browser = webdriver.Firefox(firefox_binary=FirefoxBinary(firefox_path=FIREFOX_PATH))
    #browser.implicitly_wait(30)
    return browser
    

class NewVisitorTest(LiveServerTestCase):  

    def setUp(self):  
        self.browser = build_browser()


    def tearDown(self):  
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def add_section(self,text):
        inputbox = self.browser.find_element_by_id('id_new_section')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a scene title'
        )
        inputbox.send_keys(text)
        inputbox.send_keys(u'\ue007')

        time.sleep(3)

    def test_can_start_a_list_for_one_user(self):  
        # Edith has heard about a cool new online writing app. She goes
        # to check out its homepage

        self.browser.get(self.live_server_url)

        # She notices the page title and header mention Writing
        self.assertIn('Writing', self.browser.title)  
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Writing', header_text)

        # She is invited to enter a scene (title) straight away

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an section in a to-do list table

        self.add_section('Buy peacock feathers')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another section. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)

        self.add_section('Use peacock feathers to make a fly')

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith start a new todo list
        self.browser.get(self.live_server_url)
        self.add_section('Buy peacock feathers')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = build_browser()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new section. He
        # is less interesting than Edith...
        self.add_section('Buy milk')
        self.check_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
