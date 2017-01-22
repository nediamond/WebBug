"""sniper URL Configuration

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

import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^login$', views.login_view),
    url(r'^logout$', views.logout_view),
    url(r'^hits/(?P<webbug_id>[0-9]+)/$', views.hits),
    url(r'^create$', views.create_sniper),
    url(r'^profile/$', views.user_profile),
    url(r'^new_account/$', views.new_account),
    url(r'^create_account$', views.create_account),
    url(r'^img/(?P<webbug_id>[0-9]+)/$', views.serve_bug),
    url(r'^more/(?P<hit_id>[0-9]+)/$', views.hit_details),
    url(r'^about/$', views.about)
]
