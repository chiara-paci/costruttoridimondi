import time

from unittest import skip

from . import base

class LayoutAndStylingTest(base.FunctionalTest):  

    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_section_text')
        time.sleep(self.wait_time)
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
    
        self.add_section("testing")

        inputbox = self.browser.find_element_by_id('id_section_text')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

