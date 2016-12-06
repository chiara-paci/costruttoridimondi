import os
import time
import sys

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from unittest import skip

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

GECKODRIVER_BIN = os.path.join( PARENT_DIR, 'bin' )
os.environ["PATH"]+=":"+GECKODRIVER_BIN

class FunctionalTest(StaticLiveServerTestCase):  
    firefox_path = "/usr/local/firefox/firefox"
    wait_time=1

    @classmethod
    def setUpClass(cls):  
        for arg in sys.argv:  
            if 'liveserver' in arg:  
                cls.server_url = 'http://' + arg.split('=')[1]  
                cls.liveserver=True
                return  
        super().setUpClass()  
        cls.server_url = cls.live_server_url
        cls.liveserver=False

    @classmethod
    def tearDownClass(cls):
        if cls.liveserver: return
        #print(type(cls.live_server_url))
        # if cls.server_url == cls.live_server_url:
        super().tearDownClass()

    def setUp(self):  
        self.browser = self.build_browser()

    def tearDown(self):  
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_section_inputbox(self):
        inputbox = self.browser.find_element_by_id('id_text')
        return inputbox

    def get_error_box(self):
        error = self.browser.find_element_by_css_selector('.has-error')
        return error

    def add_section(self,text):
        inputbox = self.get_section_inputbox()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a section'
        )
        inputbox.send_keys(text)
        inputbox.send_keys(u'\ue007')

        time.sleep(self.wait_time)

    def send_email(self,email):
        inputbox= self.browser.find_element_by_name('email')
        inputbox.send_keys(email)
        inputbox.send_keys(u'\ue007')
        time.sleep(self.wait_time)

    def build_browser(self):
        browser = webdriver.Firefox(firefox_binary=FirefoxBinary(firefox_path=self.firefox_path))
        #browser.implicitly_wait(30)
        return browser

