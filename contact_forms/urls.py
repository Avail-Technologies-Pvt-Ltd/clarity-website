from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_page, name='contact'),
    path('request-demo/', views.request_demo_page, name='request_demo'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
