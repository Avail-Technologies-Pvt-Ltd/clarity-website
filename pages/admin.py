from django.contrib import admin
from .models import Service, PricingPlan, Capability, FAQItem, CompanyMetric, CompanyProfile

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_email', 'contact_phone', 'office_address')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_code', 'price_min', 'price_max', 'billing_period', 'pricing_model', 'order', 'is_featured', 'is_active')
    list_editable = ('price_min', 'price_max', 'billing_period', 'order', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active')
    search_fields = ('title', 'short_description', 'full_description', 'pricing_model')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title')

@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'price_amount', 'price_annual', 'currency_symbol', 'billing_period', 'badge', 'is_featured', 'order', 'is_active')
    list_editable = ('price_amount', 'price_annual', 'order', 'is_featured', 'is_active')
    list_filter = ('plan_type', 'is_featured', 'is_active')
    search_fields = ('name', 'tagline', 'features_list')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('plan_type', 'order')

@admin.register(Capability)
class CapabilityAdmin(admin.ModelAdmin):
    list_display = ('pillar_number', 'title', 'bento_span', 'order', 'is_active')
    list_editable = ('order', 'bento_span', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'short_summary', 'full_description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', 'title')

@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('order', 'id')

@admin.register(CompanyMetric)
class CompanyMetricAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
