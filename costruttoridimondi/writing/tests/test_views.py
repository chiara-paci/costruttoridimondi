import re

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

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

    def test_home_page_redirect_after_post(self):
        response = self.client.post(
            '/writing/new',
            data={'section_text': 'A new section'}
        )
        new_story=models.Story.objects.first()
        self.assertRedirects(response, '/writing/%d/' % new_story.id)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/writing/new', data={'section_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing/home.html')
        expected_error = escape("You can't have an empty section")
        self.assertContains(response, expected_error)


class StoryViewTest(TestCase):

    def test_uses_story_template(self):
        story=models.Story.objects.create()
        response = self.client.get('/writing/%d/' % story.id )
        self.assertTemplateUsed(response, 'writing/story.html')

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

    def test_passes_correct_story_to_template(self):
        other_story = models.Story.objects.create()
        correct_story = models.Story.objects.create()
        response = self.client.get('/writing/%d/' % (correct_story.id,))
        self.assertEqual(response.context['story'], correct_story)

    def test_can_save_a_post_request_to_an_existing_story(self):
        other_story = models.Story.objects.create()
        correct_story = models.Story.objects.create()

        self.client.post(
            '/writing/%d/' % (correct_story.id,),
            data={'section_text': 'A new section for an existing story'}
        )

        self.assertEqual(models.Section.objects.count(), 1)
        new_section = models.Section.objects.first()
        self.assertEqual(new_section.text, 'A new section for an existing story')
        self.assertEqual(new_section.story, correct_story)


    def test_post_redirects_to_story_view(self):
        other_story = models.Story.objects.create()
        correct_story = models.Story.objects.create()

        response = self.client.post(
            '/writing/%d/' % (correct_story.id,),
            data={'section_text': 'A new section for an existing story'}
        )

        self.assertRedirects(response, '/writing/%d/' % (correct_story.id,))

    def test_validation_errors_are_sent_back_to_story(self):
        story=models.Story.objects.create()
        response = self.client.post('/writing/%d/' % story.id, data={'section_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'writing/story.html')
        expected_error = escape("You can't have an empty section")
        self.assertContains(response, expected_error)

    def test_invalid_section_arent_saved(self):
        self.client.post('/writing/new', data={'section_text': ''})
        self.assertEqual(models.Story.objects.count(), 0)
        self.assertEqual(models.Section.objects.count(), 0)

    def test_saving_a_post_request(self):
        self.client.post(
            '/writing/new',
            data={'section_text': 'A new section'}
        )
        self.assertEqual(models.Section.objects.count(), 1)
        new_section = models.Section.objects.first()
        self.assertEqual(new_section.text, 'A new section')


