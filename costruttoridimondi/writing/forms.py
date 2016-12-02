from django import forms

from . import models

EMPTY_SECTION_ERROR = "You can't have an empty section"

class SectionForm(forms.models.ModelForm):
    # section_text = forms.CharField(
    #     widget=forms.fields.TextInput(attrs={
    #         'placeholder': 'Enter a section',
    #         'class': "form-control input-lg"
    #     }),)
    
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
