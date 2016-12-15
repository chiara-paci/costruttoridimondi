from selenium import webdriver
from . import pages,base

class SharingTest(base.MultiuserFunctionalTest):

    def test_logged_in_users_stories_are_saved_as_my_stories(self):
        # Edith is a logged-in user
        self.set_browser('edith@example.com',size=(700,900),position=(0,0))

        # Her friend Oniciferous is also hanging out on the stories site
        oni_browser   = self.create_user_browser_with_session('oniciferous@example.com',size=(700,900),position=(700,0))

        # Edith goes to the home page and starts a list
        e_story_page = pages.HomePage(self).start_new_story('Get help')

        # She notices a "Share this story" option
        share_box = story_page.get_share_box()

        self.assertEqual(share_box.get_attribute('placeholder'),
                         'your-friend@example.com')

        # She shares her story.
        # The page updates to say that it's shared with Oniciferous:
        e_story_page.share_story_with('oniciferous@example.com')

        self.set_browser('oniciferous@example.com')

        #self.browser = oni_browser
        mystory_page=HomePage(self).go_to_home_page().click_on_mystories_link()

        o_story_page=mystory_page.click_on_story_link('Get help')

        self.wait_for(lambda: self.assertEqual(
            o_story_page.get_story_owner(),
            'edith@example.com'
        ))
        o_story_page.add_section('Hi Edith!')

        self.set_browser('edith@example.com')

        o_story_page.wait_for_new_section_in_story('Hi Edith!', 2)
