from unittest import skip

from . import base

class NewVisitorTest(base.FunctionalTest):  

    def test_can_start_a_story_for_one_user(self):  
        # Edith has heard about a cool new online writing app. She goes
        # to check out its homepage

        self.browser.get(self.server_url)

        # She notices the page title and header mention Writing
        self.assertIn('Writing', self.browser.title)  
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Start a new story', header_text)

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
        self.browser.get(self.server_url)
        self.add_section('Buy peacock feathers')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/writing/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = self.build_browser()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new section. He
        # is less interesting than Edith...
        self.add_section('Buy milk')
        self.check_for_row_in_list_table('1: Buy milk')

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/writing/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

