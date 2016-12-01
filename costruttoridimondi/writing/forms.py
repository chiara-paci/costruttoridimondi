from django import forms

class SectionForm(forms.Form):
    section_text = forms.CharField()
