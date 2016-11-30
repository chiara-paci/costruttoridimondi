from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.

from . import models

@requires_csrf_token
def home_page(request):
    return render(request, 'writing/home.html')

def view_story(request,story_id):
    story=models.Story.objects.get(id=story_id)
    return render(request, 'writing/story.html', {"story": story})

def new_story(request): 
    story=models.Story.objects.create()
    new_section_text = request.POST['section_text']  
    models.Section.objects.create(text=new_section_text,story=story)  
    return redirect("/writing/%d/" % story.id)

def add_section(request, story_id): 
    story=models.Story.objects.get(id=story_id)
    new_section_text = request.POST['section_text']  
    models.Section.objects.create(text=new_section_text,story=story)  
    return redirect("/writing/%d/" % story.id)

