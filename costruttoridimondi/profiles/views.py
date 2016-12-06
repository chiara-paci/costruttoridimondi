from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.core.urlresolvers import reverse

# Create your views here.

from . import models

def send_login_email(request):
    email = request.POST['email']
    token = models.Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token={uid}'.format(uid=str(token.uid))
    )
    message_body = 'Use this link to log in:\n\n{url}'.format(url=url)
    send_mail('Your login link for Costruttori di Mondi', 
              message_body, 'noreply@costruttoridimondi.org', [email])

    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')

def login(request):
    user=auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request,user)
    return redirect('/')

