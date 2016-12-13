from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

# Create your models here.

class Story(models.Model): 
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    def get_absolute_url(self):
        return reverse('view_story', args=[self.id])

    @staticmethod
    def create_new(first_section_text,owner=None):
        story = Story.objects.create(owner=owner)
        Section.objects.create(text=first_section_text, story=story)
        return story

    @property
    def name(self):
        return self.section_set.first().text

class Section(models.Model):
    text = models.TextField()
    story = models.ForeignKey(Story, default=None)

    class Meta:
        unique_together=("story","text")
        ordering=("id",)

    def __str__(self):
        return str(self.text)
