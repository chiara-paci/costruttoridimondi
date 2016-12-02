from unittest import skip

from . import base

class SectionValidationTest(base.FunctionalTest):  

    def test_cannot_add_empty_section(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.add_section('')

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        error = self.get_error_box()  
        self.assertEqual(error.text, "You can't have an empty section")

        # She tries again with some text for the item, which now works
        self.add_section('Buy milk')
        self.check_for_row_in_list_table('1: Buy milk')  

        # Perversely, she now decides to submit a second blank list item
        self.add_section('')

        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.get_error_box()  
        self.assertEqual(error.text, "You can't have an empty section")

        # And she can correct it by filling some text in
        self.add_section('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_sections(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.server_url)
        self.add_section('Buy wellies')
        self.check_for_row_in_list_table('1: Buy wellies')

        # She accidentally tries to enter a duplicate section
        self.add_section('Buy wellies')

        # She sees a helpful error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_box()
        self.assertEqual(error.text, "You've already got this in your story")

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a new list in a way that causes a validation error:
        self.browser.get(self.server_url)
        self.add_section("")

        error = self.get_error_box()
        self.assertTrue(error.is_displayed())  

        # She starts typing in the input box to clear the error
        inputbox = self.get_section_inputbox()
        inputbox.send_keys("a")

        # She is pleased to see that the error message disappears
        error = self.get_error_box()
        self.assertFalse(error.is_displayed()) 

