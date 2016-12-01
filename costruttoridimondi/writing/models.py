from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Story(models.Model): 

    def get_absolute_url(self):
        return reverse('view_story', args=[self.id])


class Section(models.Model):
    text = models.TextField()
    story = models.ForeignKey(Story, default=None)

