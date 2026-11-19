# urls.py — clarity_website
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from products_showcase import views as product_views
from pages import views as page_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', page_views.robots_txt, name='robots_txt'),
    path('sitemap.xml', page_views.sitemap_xml, name='sitemap_xml'),
    path('', include('pages.urls')),
    path('hardware/', product_views.hardware_list, name='hardware_root_list'),
    path('hardware/<slug:slug>/', product_views.hardware_detail, name='hardware_root_detail'),
    path('products/', include('products_showcase.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact_forms.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
