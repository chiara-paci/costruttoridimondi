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


class NewStoryForm(SectionForm): 
    def save(self,owner):
        if owner.is_authenticated:
            return models.Story.create_new(first_section_text=self.cleaned_data['text'], owner=owner)
        return models.Story.create_new(first_section_text=self.cleaned_data['text'])

            

