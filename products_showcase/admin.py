from django.contrib import admin
from .models import ProductCategory, Product, ProductPricingTier, ProductInstruction, HardwareProduct

class ProductPricingTierInline(admin.TabularInline):
    model = ProductPricingTier
    extra = 1
    fields = ('name', 'price_amount', 'price_annual', 'currency_symbol', 'billing_period', 'billing_period_annual', 'badge', 'is_featured', 'order')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


class ProductInstructionInline(admin.StackedInline):
    model = ProductInstruction
    extra = 1
    fields = ('section_number', 'title', 'category', 'instruction_type', 'severity', 'summary', 'warning_notes', 'steps_list', 'detailed_content', 'code_snippet', 'tags', 'order', 'is_active')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'badge', 'price_amount', 'billing_period', 'logo_image', 'is_featured', 'order')
    list_editable = ('price_amount', 'billing_period', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('name', 'tagline', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    inlines = [ProductPricingTierInline, ProductInstructionInline]


@admin.register(ProductPricingTier)
class ProductPricingTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'price_amount', 'price_annual', 'currency_symbol', 'billing_period', 'badge', 'is_featured', 'order')
    list_editable = ('price_amount', 'price_annual', 'billing_period', 'is_featured', 'order')
    list_filter = ('product', 'is_featured')
    search_fields = ('name', 'tagline', 'features_list')
    ordering = ('product', 'order')


@admin.register(ProductInstruction)
class ProductInstructionAdmin(admin.ModelAdmin):
    list_display = ('section_number', 'title', 'product', 'category', 'instruction_type', 'severity', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('product', 'instruction_type', 'severity', 'category', 'is_active')
    search_fields = ('section_number', 'title', 'summary', 'steps_list', 'warning_notes', 'detailed_content', 'code_snippet', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('product', 'order', 'section_number')


@admin.register(HardwareProduct)
class HardwareProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'hardware_category', 'price_min', 'price_max', 'price_unit', 'warranty', 'badge', 'is_featured', 'is_active', 'order')
    list_editable = ('price_min', 'price_max', 'price_unit', 'is_featured', 'is_active', 'order')
    list_filter = ('hardware_category', 'is_featured', 'is_active')
    search_fields = ('name', 'tagline', 'description', 'specs_list')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


