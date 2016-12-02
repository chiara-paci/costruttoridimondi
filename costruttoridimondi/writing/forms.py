from django import forms
from django.core.exceptions import ValidationError

from . import models

EMPTY_SECTION_ERROR = "You can't have an empty section"
DUPLICATE_SECTION_ERROR = "You've already got this in your story"

class SectionForm(forms.models.ModelForm):
    class Meta:
        model = models.Section
        fields = ("text",)
        widgets = {
            "text":forms.fields.TextInput(attrs={
                'placeholder': 'Enter a section',
                'class': "form-control input-lg"
            })
        }
        error_messages = {
            'text': {'required': EMPTY_SECTION_ERROR}
        }

    def save(self, for_story):
        self.instance.story = for_story
        return super().save()

class ExistingStorySectionForm(SectionForm):
    def __init__(self,for_story,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.instance.story=for_story

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_SECTION_ERROR]}
            self._update_errors(e)

