import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


import unittest

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

GECKODRIVER_BIN = os.path.join( PARENT_DIR, 'bin' )
os.environ["PATH"]+=":"+GECKODRIVER_BIN

FIREFOX_PATH = "/usr/local/firefox/firefox"

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox(firefox_binary=FirefoxBinary(firefox_path=FIREFOX_PATH))
        self.browser.implicitly_wait(30)

    def tearDown(self):  
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):  
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('Writing', self.browser.title)  

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Writing', header_text)

        # She is invited to enter a scene (title) straight away

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an section in a to-do list table

        inputbox = self.browser.find_element_by_id('id_new_section')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a scene title'
        )
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(u'\ue007')

        time.sleep(3)

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another section. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)

        inputbox2 = self.browser.find_element_by_id('id_new_section')
        self.assertEqual(
            inputbox2.get_attribute('placeholder'),
            'Enter a scene title'
        )
        inputbox2.send_keys('Use peacock feathers to make a fly')
        inputbox2.send_keys(u'\ue007')

        time.sleep(3)

        #inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both sections on her list

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        self.fail('Finish the test!')

        # The page updates again, and now shows both sections on her list

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep


if __name__ == '__main__':  
    unittest.main(warnings='ignore')  
