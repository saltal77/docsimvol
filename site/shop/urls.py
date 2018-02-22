from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.MainView, name='MainView'),
    url(r'^shop/$', views.ProductList, name='ProductList'),
    url(r'^shop/(?P<category_slug>[-\w]+)/$', views.ProductCatItemList, name='ProductListByCategory'),
    url(r'^shop/(?P<id>\d+)/(?P<slug>\d+)/$', views.ProductDetail, name='ProductDetail'),

]