from django.db import models

# Create your models here.

class Section(models.Model):
    text = models.TextField(default="")
