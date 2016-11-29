"""costruttoridimondi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import writing.views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', writing.views.home_page, name='home'),
    url(r'^writing/new$', writing.views.new_story, name='new_story'),
    url(r'^writing/the-only-story/$', writing.views.view_story, name='view_story'),
]
