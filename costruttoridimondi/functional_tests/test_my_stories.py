from unittest import skip

from . import base,pages

class MyStoriesTest(base.FunctionalTest):
    #wait_time=3

    def test_create_pre_authenticated_session(self):
        email = 'edith@example.com'
        home=pages.HomePage(self).go_to_home_page()
        self.assertTrue(home.is_logged_out_user(email))

        self.create_session(email)
        self.assertTrue(home.is_logged_in_user(email))

    def test_logged_in_users_stories_are_saved_as_my_stories(self):
        email = 'edith@example.com'
        home=pages.HomePage(self).go_to_home_page()
        self.assertTrue(home.is_logged_out_user(email))

        self.create_session(email)
        self.assertTrue(home.is_logged_in_user(email))
        
        # Edith is a logged-in user
        story_page=home.start_new_story('Reticulate splines')
        story_page.add_section('Immanentize eschaton')

        first_story_url = story_page.url()

        # She notices a "My stories" link, for the first time.
        mystories_page=story_page.click_on_mystories_link()

        # She sees that her story is in there, named according to its
        # first story item
        new_page=mystories_page.click_on_story_link("Reticulate splines")

        self.assertEqual(new_page.url(), first_story_url)

        # She decides to start another story, just to see
        story_page=pages.HomePage(self).start_new_story('Click cows')
        second_story_url = story_page.url()

        # Under "my stories", her new story appears
        mystories_page=story_page.click_on_mystories_link()
        new_page=mystories_page.click_on_story_link("Click cows")

        self.assertEqual(new_page.url(), second_story_url)

        # She logs out.  The "My stories" option disappears

        new_page=new_page.logout()

        self.assertFalse(new_page.has_my_stories())

