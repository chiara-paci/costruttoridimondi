from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

# from django.contrib.auth import get_user_model
# User = get_user_model()

from profiles import models as profiles_models

# Create your models here.

class Story(models.Model): 
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    shared_with = models.ManyToManyField("profiles.User",related_name="friend_of")

    def get_absolute_url(self):
        return reverse('view_story', args=[self.id])

    @staticmethod
    def create_new(first_section_text,owner=None):
        story = Story.objects.create(owner=owner)
        Section.objects.create(text=first_section_text, story=story)
        return story

    def share_with(self,email):
        user,created=profiles_models.User.objects.get_or_create(email=email)
        self.shared_with.add(user)

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
