from django.shortcuts import render
from products_showcase.models import Product, ProductCategory, HardwareProduct
from blog.models import Post
from .models import Service, PricingPlan, Capability, FAQItem, CompanyMetric, CompanyProfile

def home(request):
    company_profile = CompanyProfile.objects.first()
    core_products = Product.objects.filter(is_featured=True, product_type='core_product').select_related('category')
    if not core_products.exists():
        core_products = Product.objects.all().select_related('category')

    capabilities = Capability.objects.filter(is_active=True)
    featured_services = Service.objects.filter(is_featured=True, is_active=True)
    hardware_products = HardwareProduct.objects.filter(is_featured=True, is_active=True)
    metrics = CompanyMetric.objects.filter(is_active=True).order_by('order')[:4]
    latest_posts = Post.objects.filter(is_published=True).select_related('category')[:3]

    return render(request, 'pages/home.html', {
        'company_profile': company_profile,
        'core_products': core_products,
        'featured_products': core_products,
        'hardware_products': hardware_products,
        'capabilities': capabilities,
        'featured_services': featured_services,
        'metrics': metrics,
        'latest_posts': latest_posts,
    })

def what_we_do(request):
    capabilities = Capability.objects.filter(is_active=True)
    return render(request, 'pages/what_we_do.html', {
        'capabilities': capabilities,
    })

def services(request):
    service_list = Service.objects.filter(is_active=True)
    hardware_products = HardwareProduct.objects.filter(is_active=True)
    hardware_plans = PricingPlan.objects.filter(plan_type='hardware', is_active=True)
    service_plans = PricingPlan.objects.filter(plan_type='service', is_active=True)
    return render(request, 'pages/services.html', {
        'services': service_list,
        'hardware_products': hardware_products,
        'hardware_plans': hardware_plans,
        'service_plans': service_plans,
    })

def pricing(request):
    software_plans = PricingPlan.objects.filter(plan_type='software', is_active=True)
    hardware_plans = PricingPlan.objects.filter(plan_type='hardware', is_active=True)
    service_plans = PricingPlan.objects.filter(plan_type='service', is_active=True)
    products = Product.objects.prefetch_related('pricing_tiers').all()
    services = Service.objects.filter(is_active=True)
    return render(request, 'pages/pricing.html', {
        'software_plans': software_plans,
        'hardware_plans': hardware_plans,
        'service_plans': service_plans,
        'products': products,
        'services': services,
    })

def about(request):
    company_profile = CompanyProfile.objects.first()
    return render(request, 'pages/about.html', {
        'company_profile': company_profile,
    })

def faq(request):
    faq_items = FAQItem.objects.filter(is_active=True)
    return render(request, 'pages/faq.html', {
        'faq_items': faq_items,
    })

def privacy(request):
    return render(request, 'pages/privacy.html')

def terms(request):
    return render(request, 'pages/terms.html')

from django.http import HttpResponse

def robots_txt(request):
    sitemap_url = request.build_absolute_uri('/sitemap.xml')
    content = f"""User-agent: *
Allow: /
Disallow: /admin/

Sitemap: {sitemap_url}"""
    return HttpResponse(content.strip(), content_type="text/plain")

def sitemap_xml(request):
    base_url = request.build_absolute_uri('/')[:-1]
    urls = [
        {'loc': f"{base_url}/", 'changefreq': 'weekly', 'priority': '1.0'},
        {'loc': f"{base_url}/what-we-do/", 'changefreq': 'monthly', 'priority': '0.9'},
        {'loc': f"{base_url}/services/", 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{base_url}/products/", 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{base_url}/hardware/", 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{base_url}/pricing/", 'changefreq': 'weekly', 'priority': '0.85'},
        {'loc': f"{base_url}/about/", 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{base_url}/blog/", 'changefreq': 'daily', 'priority': '0.85'},
        {'loc': f"{base_url}/contact/", 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{base_url}/faq/", 'changefreq': 'monthly', 'priority': '0.7'},
        {'loc': f"{base_url}/privacy/", 'changefreq': 'yearly', 'priority': '0.3'},
        {'loc': f"{base_url}/terms/", 'changefreq': 'yearly', 'priority': '0.3'},
    ]

    for p in Product.objects.all():
        urls.append({
            'loc': f"{base_url}/products/{p.slug}/",
            'changefreq': 'weekly',
            'priority': '0.85'
        })

    for h in HardwareProduct.objects.filter(is_active=True):
        urls.append({
            'loc': f"{base_url}/hardware/{h.slug}/",
            'changefreq': 'weekly',
            'priority': '0.85'
        })

    for post in Post.objects.filter(is_published=True):
        urls.append({
            'loc': f"{base_url}/blog/{post.slug}/",
            'changefreq': 'weekly',
            'priority': '0.75'
        })

    xml_items = []
    for u in urls:
        xml_items.append(f"""  <url>
    <loc>{u['loc']}</loc>
    <changefreq>{u['changefreq']}</changefreq>
    <priority>{u['priority']}</priority>
  </url>""")

    items_str = "\n".join(xml_items)
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{items_str}
</urlset>"""
    return HttpResponse(xml_content, content_type="application/xml")
