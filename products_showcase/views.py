from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, ProductCategory, ProductInstruction, HardwareProduct

def product_list(request):
    category_slug = request.GET.get('category')
    categories = ProductCategory.objects.prefetch_related('products').all()
    products_qs = Product.objects.filter(product_type='core_product', is_featured=True).select_related('category').prefetch_related('pricing_tiers', 'instructions')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(ProductCategory, slug=category_slug)
        products_qs = products_qs.filter(category=active_category)

    return render(request, 'products_showcase/product_list.html', {
        'products': products_qs,
        'core_products': products_qs,
        'categories': categories,
        'active_category': active_category,
    })

def hardware_list(request):
    """Dedicated standalone hardware catalog for Avail Technologies turnkey equipment"""
    hardware_products = HardwareProduct.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'products_showcase/hardware_list.html', {
        'hardware_products': hardware_products,
    })

def hardware_detail(request, slug):
    """Dedicated detail page for a specific turnkey hardware product"""
    hw = get_object_or_404(HardwareProduct, slug=slug, is_active=True)
    related_hardware = HardwareProduct.objects.filter(is_active=True).exclude(id=hw.id)[:3]
    return render(request, 'products_showcase/hardware_detail.html', {
        'hw': hw,
        'related_hardware': related_hardware,
        'specs': hw.get_specs(),
        'features': hw.get_features(),
    })

def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.filter(product_type='core_product').select_related('category').prefetch_related('pricing_tiers', 'instructions'),
        slug=slug
    )
    pricing_tiers = product.pricing_tiers.all()
    instructions = product.instructions.filter(is_active=True)
    related_products = Product.objects.filter(product_type='core_product', is_featured=True).exclude(id=product.id)[:3]
    all_products = Product.objects.filter(product_type='core_product', is_featured=True).exclude(id=product.id)

    # Categories of instructions for tab filtering
    instruction_categories = instructions.values_list('category', flat=True).distinct()

    return render(request, 'products_showcase/product_detail.html', {
        'product': product,
        'pricing_tiers': pricing_tiers,
        'instructions': instructions,
        'instruction_categories': instruction_categories,
        'features': product.get_features(),
        'specs': product.get_specs(),
        'related_products': related_products,
        'all_products': all_products,
    })

def product_instructions(request, slug):
    """Dedicated searchable instructions, operational guides, and warnings portal for a product"""
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    type_filter = request.GET.get('type', '').strip()
    severity_filter = request.GET.get('severity', '').strip()

    instructions = product.instructions.filter(is_active=True)

    if query:
        instructions = instructions.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(steps_list__icontains=query) |
            Q(warning_notes__icontains=query) |
            Q(code_snippet__icontains=query) |
            Q(tags__icontains=query) |
            Q(category__icontains=query)
        )

    if category:
        instructions = instructions.filter(category=category)

    if type_filter:
        instructions = instructions.filter(instruction_type=type_filter)

    if severity_filter:
        instructions = instructions.filter(severity=severity_filter)

    all_categories = product.instructions.filter(is_active=True).values_list('category', flat=True).distinct()
    warning_count = product.instructions.filter(is_active=True, severity__in=['warning', 'critical']).count()

    return render(request, 'products_showcase/product_instructions.html', {
        'product': product,
        'instructions': instructions,
        'query': query,
        'selected_category': category,
        'selected_type': type_filter,
        'selected_severity': severity_filter,
        'all_categories': all_categories,
        'warning_count': warning_count,
        'total_count': product.instructions.filter(is_active=True).count(),
    })
