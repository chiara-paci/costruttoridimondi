import os
import time
import sys

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail

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
        cls.emaildir=None
        cls.liveserver=False
        for arg in sys.argv:  
            if 'liveserver' in arg:  
                cls.server_url = 'http://' + arg.split('=')[1]  
                cls.liveserver=True
            if 'emaildir' in arg:
                cls.emaildir = arg.split('=')[1]
        if cls.liveserver:
            return  
        super().setUpClass()  
        cls.server_url = cls.live_server_url
        cls.liveserver=False
        cls.emaildir=None

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

    def wait_for_email(self, test_email, subject):
        if not self.liveserver:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        if self.emaildir:
            return self.wait_for_email_onfile(test_email,subject)
        return self.wait_for_email_pop3(test_email,subject)

    def wait_for_email_onfile(self, test_email, subject):
        subject_line = 'Subject: {}'.format(subject)
        email_list=os.listdir(self.emaildir)
        email_list.sort()
        if not email_list: return None    
        email_file=os.path.join(self.emaildir,email_list[-1])
        fd=open(email_file,"r")
        body=fd.read()
        fd.close()
        return body
        
        # try:
        #     inbox.user(test_email)
        #     inbox.pass_(os.environ['YAHOO_PASSWORD'])
        #     while time.time() - start < 60:
        #         count, _ = inbox.stat()
        #         for i in reversed(range(max(1, count - 10), count + 1)):
        #             print('getting msg', i)
        #             _, lines, __ = inbox.retr(i)
        #             lines = [l.decode('utf8') for l in lines]
        #             print(lines)
        #             if subject_line in lines:
        #                 email_id = i
        #                 body = '\n'.join(lines)
        #                 return body
        #         time.sleep(5)
        # finally:
        #     if email_id:
        #         inbox.dele(email_id)
        #     inbox.quit()

    def wait_for_email_pop3(self, test_email, subject):
        subject_line = 'Subject: {}'.format(subject)
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ['YAHOO_PASSWORD'])
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    print(lines)
                    if subject_line in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def assert_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    def assert_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

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

