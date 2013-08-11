from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from haystack.views import SearchView

from food import views
from food.forms import CitySearchForm

urlpatterns = patterns('',
                       url(r'^$', login_required(views.IndexView.as_view()), name='index'),
                       url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
                       url(r'^(?P<restaurant_id>\d+)/grade/$', views.grade, name='grade'),
                       url(r'^addrestaurant/$', views.addrestaurant, name='addrestaurant'),
                       url(r'^(?P<restaurant_id>\d+)/editrestaurant/$', views.editrestaurant, name='editrestaurant'),
                       url(r'^(?P<restaurant_id>\d+)/adddish/$', views.adddish, name='adddish'),

                       url(r'^(?P<pk>\d+)/dishandgrade/$', views.DishAndGrade.as_view(), name='dishandgrade'),

                       url(r'^editdish/(?P<dish_id>\d+)/$', views.editdish, name='editdish'),
                       url(r'^gradedish/(?P<dish_id>\d+)/$', views.GradeDish.as_view(), name='gradedish'),

                       url(r'^search/', SearchView(form_class=CitySearchForm), name='haystack_search'),

)
