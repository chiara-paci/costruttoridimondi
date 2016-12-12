from unittest import skip

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from . import base
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

User = get_user_model()

class MyListsTest(base.FunctionalTest):

    def create_pre_authenticated_session(self, email):
        if self.liveserver:
            session_key = create_session_on_server(self.server_host, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.wait_browser()
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key, 
            path='/',
        ))

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
        self.browser.find_element_by_link_text('My stories').click()
        self.wait_browser()

        # She sees that her story is in there, named according to its
        # first story item
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.assertEqual(self.browser.current_url, first_story_url)

        # She decides to start another story, just to see
        self.browser.get(self.server_url)
        self.add_section('Click cows\n')
        second_story_url = self.browser.current_url

        # Under "my stories", her new story appears
        self.browser.find_element_by_link_text('My stories').click()
        self.wait_browser()

        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_browser()

        self.assertEqual(self.browser.current_url, second_story_url)

        # She logs out.  The "My stories" option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_browser()

        self.assertEqual(
            self.browser.find_elements_by_link_text('My stories'),
            []
        )

