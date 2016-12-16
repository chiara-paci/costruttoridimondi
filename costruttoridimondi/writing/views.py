from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

from . import models
from . import forms

@requires_csrf_token
def home_page(request):
    return render(request, 'writing/home.html', {"form": forms.SectionForm()})

def view_story(request,story_id):
    story=models.Story.objects.get(id=story_id)
    form=forms.ExistingStorySectionForm(story)
    if request.method == 'POST':
        form=forms.ExistingStorySectionForm(story,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(story)
    return render(request, 'writing/story.html', {"story": story,"form": form})

def share_story(request,story_id):
    story=models.Story.objects.get(id=story_id)
    if request.method == 'POST':
        email=request.POST["share"]
        story.share_with(email)
    return redirect(story)

def my_stories(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'writing/my_stories.html', {"owner": owner})

def new_story(request):
    form = forms.NewStoryForm(data=request.POST)  
    if form.is_valid():
        story=form.save(owner=request.user)
        return redirect(story)
    return render(request,"writing/home.html",{"form": form})

