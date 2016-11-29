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

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['section_text'] = 'A new list section'

        response = views.home_page(request)

        self.assertEqual(models.Section.objects.count(), 1)  
        new_section = models.Section.objects.first()  
        self.assertEqual(new_section.text, 'A new list section')

    def test_home_page_redirect_after_post(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['section_text'] = 'A new list section'

        response = views.home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

        # self.assertIn('A new list section', response.content.decode())

        # expected_html = render_to_string('writing/home.html',
        #                                  {'new_section_text':  'A new list section'},
        #                                  request=request)

        # self.assertEqualHtml(response.content.decode(), expected_html)

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        views.home_page(request)
        self.assertEqual(models.Section.objects.count(), 0)

    def test_home_page_displays_all_list_sections(self):
        models.Section.objects.create(text='sectioney 1')
        models.Section.objects.create(text='sectioney 2')

        request = HttpRequest()
        response = views.home_page(request)

        self.assertIn('sectioney 1', response.content.decode())
        self.assertIn('sectioney 2', response.content.decode())

class SectionModelTest(TestCase):
    def test_saving_and_retrieving_sections(self):
        first_section = models.Section()
        first_section.text = 'The first (ever) list section'
        first_section.save()

        second_section = models.Section()
        second_section.text = 'Section the second'
        second_section.save()

        saved_sections = models.Section.objects.all()
        self.assertEqual(saved_sections.count(), 2)

        first_saved_section = saved_sections[0]
        second_saved_section = saved_sections[1]
        self.assertEqual(first_saved_section.text, 'The first (ever) list section')
        self.assertEqual(second_saved_section.text, 'Section the second')
