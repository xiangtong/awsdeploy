from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^(?P<id>\d+)/?$', views.detail,name='detail'),
    url(r'^add/?$',views.add,name='add'),
    url(r'^create/?$',views.create,name='create'),
    url(r'^(?P<id>\d+)/delete/?$', views.delete,name='delete'),
    url(r'^(?P<id>\d+)/addto/?$', views.addto,name='addto'),
    url(r'^(?P<id>\d+)/remove/?$', views.remove,name='remove'),

]
