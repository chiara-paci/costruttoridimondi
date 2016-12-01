from django.test import TestCase

from .. import models

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

