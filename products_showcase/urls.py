from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('hardware/', views.hardware_list, name='hardware_list'),
    path('hardware/<slug:slug>/', views.hardware_detail, name='hardware_detail'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/instructions/', views.product_instructions, name='product_instructions'),
]
