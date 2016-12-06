from django.conf.urls import include,url

from . import views

urlpatterns = [
    url(r'^send_login_email$', views.send_login_email, name='send_login_email'),
    url(r'^login$', views.login, name='login'),
    #url(r'^logout$', views.logout, name='logout'),
]
