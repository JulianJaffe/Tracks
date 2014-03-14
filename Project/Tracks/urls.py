from django.conf.urls import patterns, include, url
from Tracks import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', views.index, name='index'),
    url(r'(?i)^$', views.tracks, name='tracks'),
    url(r'(?i)^upload/?$',views.index, name='index'),
    url(r'(?i)^upload_MP3/?$', views.upload_MP3, name='upload_MP3'),
    url(r'(?i)^signin/?$', views.signIn, name='SignIn'),
    url(r'(?i)^about.html$', views.about, name='About'),
    url(r'(?i)^register/?$', views.register, name='Register'),
    url(r'(?i)^logout/?$', views.logout_view, name='Logout'),
    url(r'(?i)^downbeat/?$', views.downbeat, name='Downbeat')
)
