from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.

from . import models

@requires_csrf_token
def home_page(request):
    return render(request, 'writing/home.html')

def view_story(request): 
    section_list=models.Section.objects.all()
    return render(request, 'writing/story.html', {"section_list": section_list})

def new_story(request): 
    story=models.Story.objects.create()
    new_section_text = request.POST['section_text']  
    models.Section.objects.create(text=new_section_text,story=story)  
    return redirect("/writing/the-only-story/")
