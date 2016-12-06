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
        # user = User.objects.create(email=email)
        # session = SessionStore()
        # session[SESSION_KEY] = user.pk 
        # session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        # session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.wait_browser()
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key, 
            path='/',
        ))

    def test_logged_in_users_stories_are_saved_as_my_stories(self):
        email = 'edith@example.com'
        self.browser.get(self.server_url)
        self.assert_logged_out(email)
        
        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.server_url)
        self.wait_browser()
        self.assert_logged_in(email)
