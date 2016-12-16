import re
import time


from . import base,pages

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Costruttori di Mondi'


class LoginTest(base.FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does

        home=pages.HomePage(self).go_to_home_page().login_request(TEST_EMAIL)

        # A message appears telling her an email has been sent

        self.assertTrue(home.email_has_sent())

        # She checks her email and finds a message
        email_msg = self.wait_for_email(TEST_EMAIL, SUBJECT)

        #self.assertIn(TEST_EMAIL, email.to)
        #self.assertEqual(email.subject, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', email_msg)
        url_search = re.search(r'http://.+/.+', email_msg)
        if not url_search:
            self.fail('Could not find url in email body:\n{}'.format(email_msg))
        url = url_search.group(0)
        self.assertIn(self.server_url, url)

        # she clicks it

        login_page=home.login(url)

        # she is logged in!
        self.assertTrue(login_page.is_logged_in_user(TEST_EMAIL))

        # Now she logs out
        new_page=login_page.logout()

        # She is logged out
        self.assertTrue(new_page.is_logged_out_user(TEST_EMAIL))
