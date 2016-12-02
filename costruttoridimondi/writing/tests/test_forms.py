from unittest import skip

from django.test import TestCase

from .. import forms
from .. import models

class SectionFormTest(TestCase):
    def test_form_renders_section_text_input(self):
        form = forms.SectionForm()
        self.assertIn('placeholder="Enter a section"', form.as_p())

    def test_form_validation_for_blank_sections(self):
        form = forms.SectionForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [forms.EMPTY_SECTION_ERROR]
        )

    def test_form_save_handles_saving_to_a_story(self):
        story=models.Story.objects.create()    
        form = forms.SectionForm(data={'text': 'do me'})
        new_section = form.save(for_story=story)
        self.assertEqual(new_section, models.Section.objects.first())
        self.assertEqual(new_section.text, 'do me')
        self.assertEqual(new_section.story, story)

    @skip
    def test_form_validation_for_duplicate_sections(self):
        story = models.Story.objects.create()
        models.Section.objects.create(story=story, text='no twins!')
        form = forms.SectionForm(data={'text': 'no twins!'})
        new_section = form.save(for_story=story)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [forms.DUPLICATE_SECTION_ERROR])


class ExistingStorySectionFormTest(TestCase):
    def test_form_renders_section_text_input(self):
        story = models.Story.objects.create()
        form = forms.ExistingStorySectionForm(for_story=story)
        self.assertIn('placeholder="Enter a section"', form.as_p())

    def test_form_validation_for_blank_sections(self):
        story = models.Story.objects.create()
        form = forms.ExistingStorySectionForm(for_story=story,data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [forms.EMPTY_SECTION_ERROR]
        )

    # def test_form_save_handles_saving_to_a_story(self):
    #     story=models.Story.objects.create()    
    #     form = forms.ExistingStorySectionForm(for_story=story,data={'text': 'do me'})
    #     new_section = form.save(for_story=story)
    #     self.assertEqual(new_section, models.Section.objects.first())
    #     self.assertEqual(new_section.text, 'do me')
    #     self.assertEqual(new_section.story, story)

    def test_form_validation_for_duplicate_sections(self):
        story = models.Story.objects.create()
        test_text='no twins!'
        models.Section.objects.create(story=story, text=test_text)
        form = forms.ExistingStorySectionForm(for_story=story, data={'text': test_text})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [forms.DUPLICATE_SECTION_ERROR])

