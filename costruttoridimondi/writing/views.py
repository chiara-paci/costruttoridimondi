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
        #section_list=models.Section.objects.all()
        #return render(request, 'writing/home.html', {"section_list": section_list})
        return redirect("/")
    section_list=models.Section.objects.all()
    return render(request, 'writing/home.html', {"section_list": section_list})

    # if request.method == 'POST':
    #     return HttpResponse(request.POST['section_text'])
    # return render(request, 'writing/home.html')
