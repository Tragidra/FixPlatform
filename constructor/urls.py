from django.contrib import admin
from django.urls import path
from constructor import views


urlpatterns = [
    path('test/', views.final_price),
    path('api/customers', views.users_list),
    path('api/customers/(?P<id>[0-9]+)$', views.users_detail),
]
