"""carte URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from carte import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signin/',views.signin,name="signin"),
    url(r'^index/',views.index,name="index"),
    url(r'^signup/',views.signup,name="signup"),
    url(r'^profile/',views.profile,name="profile"),
    url(r'^update_profile/',views.update_profile,name="update_profile"),
    url(r'^dashboard/',views.dashboard,name="dashboard"),
    url(r'^search/',views.search,name="search"),
    url(r'^logout/',views.logout_user,name="logout"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
