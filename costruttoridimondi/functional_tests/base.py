import os
import time
import sys

from unittest import skip

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.conf import settings

from .server_tools import reset_database
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))

GECKODRIVER_BIN = os.path.join( PARENT_DIR, 'bin' )
os.environ["PATH"]+=":"+GECKODRIVER_BIN

class Browser(webdriver.Firefox):
    firefox_path = "/usr/local/firefox/firefox"

    def __init__(self,wait_time=1):
        webdriver.Firefox.__init__(self,firefox_binary=FirefoxBinary(firefox_path=self.firefox_path))
        self.wait_time=1

    def wait_page(self):
        time.sleep(self.wait_time)

    def add_session(self,email,session_key,final_url):
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.get(final_url+"/404-not-found")
        self.wait_page()
        self.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key, 
            path='/',
        ))
        self.get(final_url)
        self.wait_page()
        

class FunctionalTest(StaticLiveServerTestCase):  
    wait_time=1

    def build_browser(self):
        browser = Browser(wait_time=self.wait_time)
        return browser

    def restart_browser(self):
        self.browser.quit()
        self.browser = Browser(wait_time=self.wait_time)

    @classmethod
    def setUpClass(cls):  
        cls.emaildir=None
        cls.liveserver=False
        for arg in sys.argv:  
            if 'liveserver' in arg:  
                cls.server_host = arg.split('=')[1] 
                cls.server_url = 'http://' + cls.server_host
                cls.liveserver=True
                cls.emaildir = "/srv/test.costruttoridimondi.org/var/mail"
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
        if self.liveserver:
            reset_database(self.server_host)
        self.browser = Browser(wait_time=self.wait_time)

    def tearDown(self):  
        self.browser.quit()

    def wait_for(self, function_with_assertion, timeout=-1):
        if timeout<=0: timeout=self.wait_time
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return function_with_assertion()
            except (AssertionError, WebDriverException):
                time.sleep(0.1)
        # one more try, which will raise any errors if they are outstanding
        return function_with_assertion()

    def wait_browser(self):
        time.sleep(self.wait_time)

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

    def get_session_key(self,email):
        if self.liveserver:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)
        return session_key

    def create_session(self,email):
        session_key=self.get_session_key(email)
        self.browser.add_session(email,session_key,self.server_url)

    def create_pre_authenticated_session(self, browser, email, final_url=None):
        if final_url==None: final_url=self.server_url
        session_key=self.get_session_key(email)
        browser.add_session(email,session_key,final_url)

class MultiuserFunctionalTest(FunctionalTest):
    def create_user_browser_with_session(self,email,size=None,position=None):
        user_browser = Browser(wait_time=self.wait_time)
        if email in self.browsers.keys():
            self.browsers[email].quit()
        if size: 
            w,h=size
            user_browser.set_window_size(w,h)
        if position: 
            x,y=position
            user_browser.set_window_position(x,y)
        session_key=self.get_session_key(email)
        user_browser.add_session(email,session_key,self.server_url)
        self.browsers[email]=user_browser
        return user_browser

    def set_browser(self,email,size=None,position=None):
        if email in self.browsers.keys():
            self.browser=self.browsers[email]
            if size: 
                w,h=size
                self.browser.set_window_size(w,h)
            if position: 
                x,y=position
                self.browser.set_window_position(x,y)
            return 
        kwargs={}
        if size: kwargs["size"]=size
        if position: kwargs["position"]=position
        self.browser=self.create_user_browser_with_session(email,**kwargs)

    def setUp(self):  
        if self.liveserver:
            reset_database(self.server_host)
        self.browsers = {}
        self.browser = None

    def tearDown(self):  
        for browser in self.browsers.values():
            try:
                browser.quit()
            except:
                pass

