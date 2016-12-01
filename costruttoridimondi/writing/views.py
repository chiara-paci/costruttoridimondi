from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token
from django.core.exceptions import ValidationError

# Create your views here.

from . import models

@requires_csrf_token
def home_page(request):
    return render(request, 'writing/home.html')

def view_story(request,story_id):
    story=models.Story.objects.get(id=story_id)
    error=None
    if request.method == 'POST':
        new_section_text = request.POST['section_text']  
        section=models.Section(text=new_section_text,story=story)  
        try:
            section.full_clean()
            section.save()
            return redirect("/writing/%d/" % story.id)
        except ValidationError as e:
            error="You can't have an empty section"
    return render(request, 'writing/story.html', {"story": story,"error":error})

def new_story(request): 
    story=models.Story.objects.create()
    new_section_text = request.POST['section_text']  
    section=models.Section(text=new_section_text,story=story)  
    try:
        section.full_clean()
        section.save()
    except ValidationError as e:
        story.delete()
        return render(request, 'writing/home.html',{"error":"You can't have an empty section"})
    return redirect(story)

