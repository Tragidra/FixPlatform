from django.contrib import admin
from django.urls import path, re_path
from constructor import views


urlpatterns = [
    path('test/', views.final_price),
    path('api/users', views.users_list),
    re_path(r'api/users/(?P<id>[0-9])/$', views.users_detail),
    path('api/orders', views.orders_interaction),
    re_path(r'api/orders/(?P<id>[0-9])/$', views.order_interraction),
]
