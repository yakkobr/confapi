from django.conf.urls import patterns, url

from confapi import views

urlpatterns = patterns('',
    url(r'^healthcheck/$', views.healthcheck, name='healthcheck'),
    url(r'^$', views.index, name='index'),
    url(r'^configure/$', views.configure, name='configure'),
    url(r'^use/$', views.use, name='use'),
    url(r'^extras/$', views.extras, name='extras'),
    url(r'^help/$', views.help, name='help'),
    url(r'^api_functions$', views.api_functions, name='api_functions'),
)
