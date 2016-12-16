from unittest import skip

from . import base,pages

class NewVisitorTest(base.FunctionalTest):  

    def test_can_start_a_story_for_one_user(self):  
        # Edith has heard about a cool new online writing app. She goes
        # to check out its homepage

        home=pages.HomePage(self).go_to_home_page()
        # She notices the page title and header mention Writing
        self.assertTrue(home.has_win_title('Writing'))

        # She is invited to enter a scene (title) straight away
        self.assertTrue(home.has_title('Start a new story'))

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an section in a to-do list table

        story_page=home.add_section('Buy peacock feathers')
        story_page.check_for_row_in_story_table('Buy peacock feathers',1)

        # There is still a text box inviting her to add another section. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)

        story_page.add_section('Use peacock feathers to make a fly')
        story_page.check_for_row_in_story_table('Buy peacock feathers',1)
        story_page.check_for_row_in_story_table('Use peacock feathers to make a fly',2)

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith start a new todo list
        home=pages.HomePage(self).go_to_home_page()
        story_page=home.add_section('Buy peacock feathers')
        story_page.check_for_row_in_story_table('Buy peacock feathers',1)

        # She notices that her list has a unique URL
        edith_list_url = story_page.url()
        self.assertRegex(edith_list_url, '/writing/.+')

        # Now a new user, Francis, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc

        self.restart_browser()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        home=pages.HomePage(self).go_to_home_page()

        page_text=home.body()
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new section. He
        # is less interesting than Edith...
        story_page=home.add_section('Buy milk')
        story_page.check_for_row_in_story_table('Buy milk',1)

        # Francis gets his own unique URL
        francis_list_url = story_page.url()
        self.assertRegex(francis_list_url, '/writing/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text=story_page.body()
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

