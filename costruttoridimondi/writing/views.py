from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.

from . import models

@requires_csrf_token
def home_page(request):
    if request.method == 'POST':
        new_section_text = request.POST['section_text']  
        models.Section.objects.create(text=new_section_text)  
        return redirect("/writing/the-only-story/")
    return render(request, 'writing/home.html')

def view_list(request): 
    section_list=models.Section.objects.all()
    return render(request, 'writing/list.html', {"section_list": section_list})
