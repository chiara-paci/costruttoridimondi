from django.test import TestCase
from django.core.exceptions import ValidationError

from .. import models

class StoryModelTest(TestCase):
    def test_get_absolute_url(self):
        story = models.Story.objects.create()
        self.assertEqual(story.get_absolute_url(), '/writing/%d/' % (story.id,))

class SectionModelTest(TestCase):
    def test_default_text(self):
        section = models.Section()
        self.assertEqual(section.text, '')

    def test_section_is_related_to_story(self):
        story = models.Story.objects.create()
        section = models.Section()
        section.story = story
        section.save()
        self.assertIn(section, story.section_set.all())

    # def test_saving_and_retrieving_sections(self):
    #     story=models.Story()
    #     story.save()

    #     first_section = models.Section()
    #     first_section.text = 'The first (ever) story section'
    #     first_section.story = story
    #     first_section.save()

    #     second_section = models.Section()
    #     second_section.text = 'Section the second'
    #     second_section.story = story
    #     second_section.save()

    #     saved_story=models.Story.objects.first()
    #     self.assertEqual(saved_story,story)

    #     saved_sections = models.Section.objects.all()
    #     self.assertEqual(saved_sections.count(), 2)

    #     first_saved_section = saved_sections[0]
    #     second_saved_section = saved_sections[1]
    #     self.assertEqual(first_saved_section.text, 'The first (ever) story section')
    #     self.assertEqual(first_saved_section.story, story)
    #     self.assertEqual(second_saved_section.text, 'Section the second')
    #     self.assertEqual(second_saved_section.story, story)

    def test_cannot_save_empty_sections(self):
        story = models.Story.objects.create()
        section = models.Section(story=story, text='')
        with self.assertRaises(ValidationError):
            section.save()
            section.full_clean()

    def test_duplicate_sections_are_invalid(self):
        story = models.Story.objects.create()
        models.Section.objects.create(story=story, text='bla')
        with self.assertRaises(ValidationError):
            section = models.Section(story=story, text='bla')
            section.full_clean()
            #section.save()

    def test_can_save_same_section_to_different_stories(self):
        story1 = models.Story.objects.create()
        story2 = models.Story.objects.create()
        models.Section.objects.create(story=story1, text='bla')
        section = models.Section(story=story2, text='bla')
        section.full_clean()  # should not raise

    def test_story_ordering(self):
        story1 = models.Story.objects.create()
        section1 = models.Section.objects.create(story=story1, text='i1')
        section2 = models.Section.objects.create(story=story1, text='section 2')
        section3 = models.Section.objects.create(story=story1, text='3')
        self.assertEqual(
            list(models.Section.objects.all()),
            [section1, section2, section3]
        )

    def test_string_representation(self):
        section = models.Section(text='some text')
        self.assertEqual(str(section), 'some text')
