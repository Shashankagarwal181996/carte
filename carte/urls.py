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
from django.conf.urls import url,include
from django.conf.urls.static import static
from carte import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^$', views.index,name="indexs"),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',views.signin,name="signin"),
    url(r'^index/',views.index,name="index"),
    # url(r'',views.index,name="index"),
    url(r'^register/',views.register,name="register"),
    url(r'^signup/',views.signup,name="signup"),
    url(r'^profile/',views.profile,name="profile"),
    url(r'^update_profile/',views.update_profile,name="update_profile"),
    url(r'^dashboard/',views.dashboard,name="dashboard"),
    url(r'^detail/(?P<name>[a-z,A-Z,0-9-,-,&]+)/',views.product_detail,name="detail"),
    url(r'^add-review/(?P<name>[a-z,A-Z,0-9-,-,&]+)/',views.add_review,name="add_review"),
    url(r'^search/',views.search,name="search"),
    url(r'^logout/',views.logout_user,name="logout"),
    url(r'^contact-us/',views.contact_us,name="contact_us"),
    url(r'^about-us/',views.about_us,name="contact_us"),

    # url('', include('social.apps.django_app.urls', namespace='social')),
    # url('', include('django.contrib.auth.urls', namespace='auth')),

    # url('', include('social.apps.django_app.urls', namespace='social')),
    
    # url(r'^user/password/reset/$', 
    #     'django.contrib.auth.views.password_reset', 
    #     {'post_reset_redirect' : '/user/password/reset/done/'},
    #     name="password_reset"),

    # url(r'^user/password/reset/done/$',
    #     'django.contrib.auth.views.password_reset_done'),
    
    # url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
    #     'django.contrib.auth.views.password_reset_confirm', 
    #     {'post_reset_redirect' : '/user/password/done/'}),
    
    # url(r'^user/password/done/$', 
    #     'django.contrib.auth.views.password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

