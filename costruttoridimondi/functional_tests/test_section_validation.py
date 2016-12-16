from unittest import skip

from . import base,pages

class SectionValidationTest(base.FunctionalTest):  

    #wait_time=2

    def test_cannot_add_empty_section(self):

        # Edith goes to the home page and accidentally tries to submit
        # an empty story item. She hits Enter on the empty input box
        # The home page refreshes, and there is an error message saying
        # that story items cannot be blank

        home=pages.HomePage(self).go_to_home_page()
        new_page=home.add_empty_section()

        # She tries again with some text for the item, which now works
        story_page=new_page.add_section('Buy milk')

        # Perversely, she now decides to submit a second blank story item
        # She receives a similar warning on the story page

        story_page=story_page.add_empty_section()

        # And she can correct it by filling some text in
        story_page=story_page.add_section("Make tea")
        story_page.check_for_row_in_story_table('Buy milk',1)
        story_page.check_for_row_in_story_table('Make tea',2)

    def test_cannot_add_duplicate_sections(self):
        # Edith goes to the home page and starts a new story
        home=pages.HomePage(self).go_to_home_page()
        story_page=home.add_section('Buy wellies')
        story_page.check_for_row_in_story_table('Buy wellies',1)

        # She accidentally tries to enter a duplicate section
        # She sees a helpful error message
        story_page.add_duplicate_section('Buy wellies',1)

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a new story in a way that causes a validation error:
        # self.browser.get(self.server_url)
        # self.add_section("")
        home=pages.HomePage(self).go_to_home_page()
        new_page=home.add_empty_section()

        error = new_page.get_error_box()
        self.assertTrue(error.is_displayed())  

        # She starts typing in the input box to clear the error
        inputbox = new_page.get_section_input()
        inputbox.send_keys("a")

        # She is pleased to see that the error message disappears
        error = new_page.get_error_box()
        self.assertFalse(error.is_displayed()) 

