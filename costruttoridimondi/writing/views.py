from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token
from django.core.exceptions import ValidationError

# Create your views here.

from . import models
from . import forms

@requires_csrf_token
def home_page(request):
    return render(request, 'writing/home.html', {"form": forms.SectionForm()})

def view_story(request,story_id):
    story=models.Story.objects.get(id=story_id)
    form=forms.SectionForm()
    if request.method == 'POST':
        form=forms.SectionForm(data=request.POST)
        if form.is_valid():
            form.save(for_story=story)
            return redirect(story)
    return render(request, 'writing/story.html', {"story": story,"form": form})

def new_story(request): 
    form = forms.SectionForm(data=request.POST)  
    if form.is_valid():  
        story=models.Story.objects.create()
        form.save(for_story=story)
        return redirect(story)
    return render(request, 'writing/home.html', {"form": form}) 


