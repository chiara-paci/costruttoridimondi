from unittest import skip

from . import base,pages

class LayoutAndStylingTest(base.FunctionalTest):  
    #wait_time=1

    def test_layout_and_styling(self):
        self.browser.set_window_size(1024,768)

        home=pages.HomePage(self).go_to_home_page()
        inputbox=home.get_section_input()

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
    
        story_page=home.start_new_story("testing")
        inputbox=story_page.get_section_input()

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

