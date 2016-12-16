from unittest import skip
import collections

from django.test import TestCase
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

from .. import models

class StoryModelTest(TestCase):
    def test_get_absolute_url(self):
        story = models.Story.objects.create()
        self.assertEqual(story.get_absolute_url(), '/writing/%d/' % (story.id,))

    def test_create_new_creates_story_and_first_section(self):
        models.Story.create_new(first_section_text='new section text')
        new_section = models.Section.objects.first()
        self.assertEqual(new_section.text, 'new section text')
        new_story = models.Story.objects.first()
        self.assertEqual(new_section.story, new_story)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        models.Story.create_new(first_section_text='new section text', owner=user)
        new_story = models.Story.objects.first()
        self.assertEqual(new_story.owner, user)

    def test_stories_can_have_owners(self):
        models.Story(owner=User())  # should not raise

    def test_story_owner_is_optional(self):
        models.Story().full_clean()  # should not raise

    def test_create_returns_new_story_object(self):
        returned = models.Story.create_new(first_section_text='new section text')
        new_story = models.Story.objects.first()
        self.assertEqual(returned, new_story)

    def test_story_name_is_first_section_text(self):
        story = models.Story.objects.create()
        models.Section.objects.create(story=story, text='first section')
        models.Section.objects.create(story=story, text='second section')
        self.assertEqual(story.name, 'first section')

    def test_mock_view_share_with_method(self): 
        story = models.Story.objects.create()
        self.assertTrue(hasattr(story,"share_with"))
        self.assertTrue(callable(story.share_with))
        story.share_with("prova@pinco.pallo.it") # should not raise

    def test_template_has_shared_with_all(self):
        story = models.Story.objects.create()
        self.assertTrue(hasattr(story,"shared_with"))
        self.assertTrue(hasattr(story.shared_with,"all"))
        self.assertTrue(callable(story.shared_with.all))
        L=story.shared_with.all()
        self.assertTrue(isinstance(L,collections.Iterable))

    def test_share_with_add_a_new_user_if_not_exists(self):
        owner=User.objects.create(email="owner@example.com")
        story=models.Story.objects.create(owner=owner)
        self.assertEqual(User.objects.count(),1)
        story.share_with("unknown@example.com")
        self.assertEqual(User.objects.count(),2)
        newuser=User.objects.last()
        self.assertEqual(newuser.email,"unknown@example.com")

    def test_share_with_add_an_old_user_if_exists(self):
        owner=User.objects.create(email="owner@example.com")
        friend=User.objects.create(email="friend@example.com")
        story=models.Story.objects.create(owner=owner)
        self.assertEqual(User.objects.count(),2)
        story.share_with("friend@example.com")
        self.assertEqual(User.objects.count(),2)
        
    def test_share_with_add_a_friend_to_shared_with(self):
        owner=User.objects.create(email="owner@example.com")
        friend=User.objects.create(email="friend@example.com")
        story=models.Story.objects.create(owner=owner)
        self.assertEqual(story.shared_with.all().count(),0)
        story.share_with(friend.email)
        self.assertEqual(story.shared_with.all().count(),1)
        self.assertEqual(story.shared_with.all().first(),friend)        

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

