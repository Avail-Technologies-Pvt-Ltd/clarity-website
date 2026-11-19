from django.contrib import admin
from .models import ContactInquiry, DemoRequest, NewsletterSubscriber, MeetingBooking

@admin.register(MeetingBooking)
class MeetingBookingAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'name', 'meeting_topic', 'meeting_format', 'preferred_date', 'preferred_time_slot', 'status', 'created_at')
    list_filter = ('status', 'meeting_format', 'preferred_date', 'created_at')
    search_fields = ('company_name', 'name', 'email', 'phone', 'meeting_topic', 'notes')
    readonly_fields = ('created_at',)

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'inquiry_type', 'status', 'created_at')
    list_filter = ('status', 'inquiry_type', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('created_at',)

@admin.register(DemoRequest)
class DemoRequestAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'name', 'business_type', 'store_count', 'product_interest', 'is_contacted', 'created_at')
    list_filter = ('is_contacted', 'business_type', 'store_count', 'created_at')
    search_fields = ('company_name', 'name', 'email', 'phone', 'notes')
    readonly_fields = ('created_at',)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
