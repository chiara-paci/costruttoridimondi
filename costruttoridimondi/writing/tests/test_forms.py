import unittest

from unittest import skip
from unittest.mock import patch,Mock
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

    def test_form_save(self):
        story = models.Story.objects.create()
        form = forms.ExistingStorySectionForm(story, data={'text': 'hi'})
        new_item = form.save()
        self.assertEqual(new_item, models.Section.objects.all()[0])


class NewStoryFormTest(unittest.TestCase):
    @patch('writing.forms.models.Story.create_new')
    def test_save_creates_new_story_from_post_data_if_user_not_authenticated(self, mock_Story_create_new):
        user = Mock(is_authenticated=False)
        form = forms.NewStoryForm(data={'text': 'new section text'})
        form.is_valid()
        form.save(owner=user)
        mock_Story_create_new.assert_called_once_with(first_section_text='new section text')

    @patch('writing.forms.models.Story.create_new')
    def test_save_creates_new_story_with_owner_if_user_authenticated(self, mock_Story_create_new):
        user = Mock(is_authenticated=True)
        form = forms.NewStoryForm(data={'text': 'new section text'})
        form.is_valid()
        form.save(owner=user)
        mock_Story_create_new.assert_called_once_with(first_section_text='new section text', 
                                                      owner=user)

        
    @patch('writing.forms.models.Story.create_new')
    def test_save_returns_new_story_object(self, mock_Story_create_new):
        user = Mock(is_authenticated=True)
        form = forms.NewStoryForm(data={'text': 'new section text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_Story_create_new.return_value)
