from django.contrib import admin
from django.urls import path, re_path
from constructor import views


urlpatterns = [
    path('test/', views.final_price),
    path('api/users', views.users_list),
    path('api/users/<int:id>/', views.users_detail),
    path('api/orders', views.orders_interaction),
    path('api/orders/<int:id>/', views.order_interraction),
    path('api/orders', views.orders_interaction),
    path('api/authorize', views.authorize),
    path('api/additionalWorks', views.check_fields_list),
    path('api/additionalWorks/<int:id>/$', views.check_fields_detail),
    path('api/payments', views.payments_list),
    path('api/payments/<int:id>/$', views.payments_details),
    path('api/qr', views.create_qr),
    path('api/chats', views.chats_list),
    path('api/chats/<int:id>/$', views.chats_details),
    path('api/chatTexts', views.chat_texts_list),
    path('api/chatTexts/<int:id>/$', views.chat_texts_details),
    path('api/passports', views.passports_list),
    path('api/passports/<int:id>/$', views.passports_details),
    path('api/refferals', views.passports_details),
]
