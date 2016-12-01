from django.test import TestCase

from .. import forms

class SectionFormTest(TestCase):

    def test_form_renders_section_text_input(self):
        form = forms.SectionForm()
        self.fail(form.as_p())
