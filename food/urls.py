from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from haystack.views import SearchView

from food import views
from food.forms import CitySearchForm

urlpatterns = patterns('',
                       url(r'^$',login_required(views.home),name='home'),
                       url(r'^restaurants$', login_required(views.IndexView.as_view()), name='restaurants'),
                       url(r'^(?P<pk>\d+)/$', login_required(views.DetailView.as_view()), name='detail'),
                       url(r'^(?P<restaurant_id>\d+)/grade/$', views.grade, name='grade'),
                       url(r'^addrestaurant/$', views.addrestaurant, name='addrestaurant'),
                       url(r'^(?P<restaurant_id>\d+)/editrestaurant/$', views.editrestaurant, name='editrestaurant'),
                       url(r'^(?P<restaurant_id>\d+)/adddish/$', views.adddish, name='adddish'),

                       url(r'^(?P<pk>\d+)/dishandgrade/$', views.DishAndGrade.as_view(), name='dishandgrade'),

                       url(r'^editdish/(?P<dish_id>\d+)/$', views.editdish, name='editdish'),
                       url(r'^gradedish/(?P<dish_id>\d+)/$', views.GradeDish.as_view(), name='gradedish'),

                       #  url conf creates a view for this url. SearchView is a class of views(imported above),
                       #  and we customize it by
                       #giving it a form, and a template. IF we do not give it a template, then it will look for and use
                       #search.html
                       #to summarize - what urlconf does: what url, what view, what template, what form
                       url(r'^search/', SearchView(form_class=CitySearchForm), name='haystack_search'),

)
