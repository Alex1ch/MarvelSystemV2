from django.conf.urls import  url
from MarvelComixStore import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^comic_view/(?P<id>[0-9])',views.ComicsView.as_view()),
    url(r'^marvel',views.Search.as_view(),name='marvel'),
    url(r'^comics/(?P<username>\w+)',views.Comics.as_view(),name='comics'),
    url(r'^get_added',views.get_added),
    url(r'^auth',auth_views.login, {'template_name': 'auth.html'}, name='login'),
    url(r'^logout',auth_views.logout,{'next_page': '/marvel'}),
    url(r'^add/(?P<id>[0-9]+)',views.add),
    url(r'^delete/(?P<id>[0-9]+)',views.delete),
    url(r'^master',views.Master.as_view(), name='master')
    #url(r'^',views.Index.as_view()),

]
