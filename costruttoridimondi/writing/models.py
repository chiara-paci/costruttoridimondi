from django.db import models

# Create your models here.

class Story(models.Model): pass

class Section(models.Model):
    text = models.TextField()
    story = models.ForeignKey(Story, default=None)

