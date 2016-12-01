from django.test import TestCase

from .. import forms

class SectionFormTest(TestCase):

    def test_form_section_input_has_placeholder_and_css_classes(self):
        form = forms.SectionForm()
        self.assertIn('placeholder="Enter a section"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_sections(self):
        form = forms.SectionForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [forms.EMPTY_SECTION_ERROR]
        )

