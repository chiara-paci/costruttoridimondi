import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

GECKODRIVER_BIN = os.path.join( PARENT_DIR, 'bin' )
os.environ["PATH"]+=":"+GECKODRIVER_BIN

FIREFOX_PATH = "/usr/local/firefox/firefox"

browser = webdriver.Firefox(firefox_binary=FirefoxBinary(
    firefox_path=FIREFOX_PATH
))


#browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

