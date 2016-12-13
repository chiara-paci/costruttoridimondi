from unittest import skip

from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from . import base

User = get_user_model()

class MyListsTest(base.FunctionalTest):

    def test_create_pre_authenticated_session(self):
        email = 'edith@example.com'
        self.browser.get(self.server_url)
        self.assert_logged_out(email)
        
        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self.wait_browser()
        self.assert_logged_in(email)

    def test_logged_in_users_stories_are_saved_as_my_stories(self):
        email = 'edith@example.com'
        self.browser.get(self.server_url)
        self.assert_logged_out(email)
        
        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self.add_section('Reticulate splines\n')
        self.add_section('Immanentize eschaton\n')
        first_story_url = self.browser.current_url

        # She notices a "My stories" link, for the first time.
        self.click_on_link("My stories")

        # She sees that her story is in there, named according to its
        # first story item
        self.click_on_link("Reticulate splines")
        self.assertEqual(self.browser.current_url, first_story_url)

        # She decides to start another story, just to see
        self.browser.get(self.server_url)
        self.add_section('Click cows\n')
        second_story_url = self.browser.current_url

        # Under "my stories", her new story appears
        self.click_on_link("My stories")
        self.click_on_link("Click cows")

        self.assertEqual(self.browser.current_url, second_story_url)

        # She logs out.  The "My stories" option disappears
        self.click_on_link("Log out")

        self.assertEqual(
            self.browser.find_elements_by_link_text('My stories'),
            []
        )

