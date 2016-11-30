import re

from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from . import views
from . import models

class HomePageTest(TestCase):
    def assertEqualHtml(self,html_a,html_b):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        html_a=re.sub(csrf_regex, '<input type="hidden" name="csrfmiddlewaretoken" value="">', html_a)
        html_b=re.sub(csrf_regex, '<input type="hidden" name="csrfmiddlewaretoken" value="">', html_b)
        self.assertEqual(html_a,html_b)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, views.home_page)  

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  
        response = views.home_page(request)  
        expected_html = render_to_string('writing/home.html',request=request)
        self.assertEqualHtml(response.content.decode(),expected_html)

class NewStoryTest(TestCase):
    def test_saving_a_post_request(self):
        self.client.post(
            '/writing/new',
            data={'section_text': 'A new section'}
        )
        self.assertEqual(models.Section.objects.count(), 1)
        new_section = models.Section.objects.first()
        self.assertEqual(new_section.text, 'A new section')


    def test_home_page_redirect_after_post(self):
        response = self.client.post(
            '/writing/new',
            data={'section_text': 'A new section'}
        )

        self.assertRedirects(response, '/writing/the-only-story/')


class SectionAndStoryModelTest(TestCase):
    def test_saving_and_retrieving_sections(self):
        story=models.Story()
        story.save()

        first_section = models.Section()
        first_section.text = 'The first (ever) story section'
        first_section.story = story
        first_section.save()

        second_section = models.Section()
        second_section.text = 'Section the second'
        second_section.story = story
        second_section.save()

        saved_story=models.Story.objects.first()
        self.assertEqual(saved_story,story)

        saved_sections = models.Section.objects.all()
        self.assertEqual(saved_sections.count(), 2)

        first_saved_section = saved_sections[0]
        second_saved_section = saved_sections[1]
        self.assertEqual(first_saved_section.text, 'The first (ever) story section')
        self.assertEqual(first_saved_section.story, story)
        self.assertEqual(second_saved_section.text, 'Section the second')
        self.assertEqual(second_saved_section.story, story)

class StoryViewTest(TestCase):

    def test_uses_story_template(self):
        response = self.client.get('/writing/the-only-story/')
        self.assertTemplateUsed(response, 'writing/story.html')

    def test_displays_all_sections(self):
        story=models.Story.objects.create()
        models.Section.objects.create(text='sectioney 1',story=story)
        models.Section.objects.create(text='sectioney 2',story=story)

        response = self.client.get('/writing/the-only-story/')  

        self.assertContains(response, 'sectioney 1')  
        self.assertContains(response, 'sectioney 2') 
