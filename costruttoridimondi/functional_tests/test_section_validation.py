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

        error = self.browser.find_element_by_css_selector('.has-error')  
        self.assertEqual(error.text, "You can't have an empty section")

        # She tries again with some text for the item, which now works
        self.add_section('Buy milk')
        self.check_for_row_in_list_table('1: Buy milk')  

        # Perversely, she now decides to submit a second blank list item
        self.add_section('')

        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')  
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling some text in
        self.add_section('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

