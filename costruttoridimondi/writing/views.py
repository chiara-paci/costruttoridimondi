from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token

# Create your views here.

@requires_csrf_token
def home_page(request):
    return render(request, 'writing/home.html', {
        'new_item_text': request.POST.get('item_text','')
    })
    # if request.method == 'POST':
    #     return HttpResponse(request.POST['item_text'])
    # return render(request, 'writing/home.html')
