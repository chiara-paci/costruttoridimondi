import re
import unittest
from unittest import skip
from unittest.mock import patch,Mock

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
from django.contrib.auth import get_user_model

User = get_user_model()

from .. import views
from .. import models
from .. import forms

class HomePageTest(TestCase):
    maxDiff=None

    def assertEqualHtml(self,html_a,html_b):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        html_a=re.sub(csrf_regex, '<input type="hidden" name="csrfmiddlewaretoken" value="">', html_a)
        html_b=re.sub(csrf_regex, '<input type="hidden" name="csrfmiddlewaretoken" value="">', html_b)
        self.assertMultiLineEqual(html_a,html_b)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'writing/home.html')  

    def test_home_page_uses_section_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], forms.SectionForm)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/writing/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/writing/new', data={'text': ''})
        self.assertContains(response, escape(forms.EMPTY_SECTION_ERROR))

    def test_saving_a_post_request(self):
        self.client.post(
            '/writing/new',
            data={'text': 'A new section'}
        )
        self.assertEqual(models.Section.objects.count(), 1)
        new_section = models.Section.objects.first()
        self.assertEqual(new_section.text, 'A new section')

class NewStoryViewIntegratedTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/writing/new', data={'text': 'A new story section'})
        self.assertEqual(models.Section.objects.count(), 1)
        new_section = models.Section.objects.first()
        self.assertEqual(new_section.text, 'A new story section')

    def test_for_invalid_input_doesnt_save_but_shows_errors(self):
        response = self.client.post('/writing/new', data={'text': ''})
        self.assertEqual(models.Story.objects.count(), 0)
        self.assertContains(response, escape(forms.EMPTY_SECTION_ERROR))

    def test_story_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/writing/new', data={'text': 'new section'})
        story = models.Story.objects.first()
        self.assertEqual(story.owner, user)

class StoryViewTest(TestCase):

    def post_invalid_input(self):
        story=models.Story.objects.create()
        response = self.client.post('/writing/%d/' % story.id, data={'text': ''})
        return response

    ## ok
    def test_uses_story_template(self):
        story=models.Story.objects.create()
        response = self.client.get('/writing/%d/' % story.id )
        self.assertTemplateUsed(response, 'writing/story.html')

    ## ok
    def test_displays_only_sections_for_that_story(self):
        story=models.Story.objects.create()
        models.Section.objects.create(text='sectioney 1',story=story)
        models.Section.objects.create(text='sectioney 2',story=story)

        story2=models.Story.objects.create()
        models.Section.objects.create(text='sectioney 3',story=story2)
        models.Section.objects.create(text='sectioney 4',story=story2)

        response = self.client.get('/writing/%d/' % story.id )  

        self.assertContains(response, 'sectioney 1')  
        self.assertContains(response, 'sectioney 2') 
        self.assertNotContains(response, 'sectioney 3')  
        self.assertNotContains(response, 'sectioney 4') 

    ## ok
    def test_passes_correct_story_to_template(self):
        other_story = models.Story.objects.create()
        correct_story = models.Story.objects.create()
        response = self.client.get('/writing/%d/' % (correct_story.id,))
        self.assertEqual(response.context['story'], correct_story)

    ## ok
    def test_can_save_a_post_request_to_an_existing_story(self):
        other_story = models.Story.objects.create()
        correct_story = models.Story.objects.create()

        self.client.post(
            '/writing/%d/' % (correct_story.id,),
            data={'text': 'A new section for an existing story'}
        )

        self.assertEqual(models.Section.objects.count(), 1)
        new_section = models.Section.objects.first()
        self.assertEqual(new_section.text, 'A new section for an existing story')
        self.assertEqual(new_section.story, correct_story)


    ## ok
    def test_post_redirects_to_story_view(self):
        other_story = models.Story.objects.create()
        correct_story = models.Story.objects.create()

        response = self.client.post(
            '/writing/%d/' % (correct_story.id,),
            data={'text': 'A new section for an existing story'}
        )

        self.assertRedirects(response, '/writing/%d/' % (correct_story.id,))

    ## ok
    def test_displays_section_form(self):
        story = models.Story.objects.create()
        response = self.client.get('/writing/%d/' % (story.id,))
        self.assertIsInstance(response.context['form'], forms.ExistingStorySectionForm)
        self.assertContains(response, 'name="text"')

    ## ok
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(models.Section.objects.count(), 0)

    ## ok
    def test_for_invalid_input_renders_story_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing/story.html')

    ## ok
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], forms.SectionForm)

    ## ok
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(forms.EMPTY_SECTION_ERROR))

    ## ok
    def test_duplicate_section_validation_errors_end_up_on_story_page(self):
        story1 = models.Story.objects.create()
        section1 = models.Section.objects.create(story=story1, text='textey')

        response = self.client.post(
            '/writing/%d/' % (story1.id,),
            data={'text': 'textey'}
        )

        expected_error = escape(forms.DUPLICATE_SECTION_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'writing/story.html')
        self.assertEqual(models.Section.objects.all().count(), 1)

class MyStoriesTest(TestCase):

    def test_my_stories_url_renders_my_stories_template(self):
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/writing/users/a@b.com/')
        self.assertTemplateUsed(response, 'writing/my_stories.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/writing/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)


@patch('writing.views.forms.NewStoryForm')  
class NewStoryViewUnitTest(unittest.TestCase):  

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new story section'  
        self.request.user = Mock()

    def test_passes_POST_data_to_NewStoryForm(self, mockNewStoryForm):
        views.new_story(self.request)
        mockNewStoryForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewStoryForm):
        mock_form = mockNewStoryForm.return_value
        mock_form.is_valid.return_value = True
        views.new_story(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('writing.views.redirect')  
    def test_redirects_to_form_returned_object_if_form_valid(self, mock_redirect, mockNewStoryForm  ):
        mock_form = mockNewStoryForm.return_value
        mock_form.is_valid.return_value = True  
        response = views.new_story(self.request)
        self.assertEqual(response, mock_redirect.return_value)  
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('writing.views.render')  
    def test_renders_home_template_with_form_if_form_invalid(self, mock_render, mockNewStoryForm  ):
        mock_form = mockNewStoryForm.return_value
        mock_form.is_valid.return_value = False  
        response = views.new_story(self.request)
        self.assertEqual(response, mock_render.return_value)  
        mock_render.assert_called_once_with(self.request, 'writing/home.html', {'form': mock_form})

    def test_does_not_save_if_form_invalid(self, mockNewStoryForm):
        mock_form = mockNewStoryForm.return_value
        mock_form.is_valid.return_value = False
        views.new_story(self.request)
        self.assertFalse(mock_form.save.called)
