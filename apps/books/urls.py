from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^add/?$',views.add, name='add'),
  url(r'^create/(?P<id>\d*)/?$',views.create, name='create'),
  url(r'^(?P<id>\d+)/?$',views.detail, name='detail'),
  url(r'^(?P<id>\d+)/delete/?$',views.delete, name='delete'),
]
