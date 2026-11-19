from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('what-we-do/', views.what_we_do, name='what_we_do'),
    path('services/', views.services, name='services'),
    path('pricing/', views.pricing, name='pricing'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]
