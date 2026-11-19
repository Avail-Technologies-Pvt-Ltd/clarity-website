from django.db import models

class ContactInquiry(models.Model):
    INQUIRY_CHOICES = [
        ('demo', 'Request a Live Demo'),
        ('sales', 'Sales & Pricing Inquiry'),
        ('hardware', 'Hardware & POS Terminal Bundles'),
        ('support', 'Technical Support'),
        ('partnership', 'Partner / Distributor Program'),
        ('other', 'General Inquiry'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_review', 'In Review'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=150, blank=True)
    inquiry_type = models.CharField(max_length=30, choices=INQUIRY_CHOICES, default='demo')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_inquiry_type_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class DemoRequest(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('motor_spares_retail', 'Motor Spares Retailer / Auto Parts Shop'),
        ('motor_spares_wholesale', 'Motor Spares Wholesaler / Bulk Depot'),
        ('hostel', 'Student Hostel / Accommodation'),
        ('events', 'Events, Conferences & Exhibitions'),
        ('workshop_fleet', 'Automotive Workshop & Fleet Depot'),
        ('other', 'Other Business Type'),
    ]

    STORE_COUNT_CHOICES = [
        ('1', '1 Store / Branch'),
        ('2-5', '2 - 5 Stores'),
        ('6-20', '6 - 20 Stores'),
        ('20+', '20+ Enterprise Stores'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company_name = models.CharField(max_length=150)
    business_type = models.CharField(max_length=40, choices=BUSINESS_TYPE_CHOICES, default='motor_spares_retail')
    store_count = models.CharField(max_length=20, choices=STORE_COUNT_CHOICES, default='1')
    product_interest = models.CharField(max_length=200, default='Clarity Retail Suite', help_text="e.g. Retail LAN, Retail Hub, Wholesale")
    preferred_timeframe = models.CharField(max_length=100, blank=True, help_text="e.g. Immediately, Next Week")
    notes = models.TextField(blank=True)
    is_contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demo Request"
        verbose_name_plural = "Demo Requests"
        ordering = ['-created_at']

    def __str__(self):
        return f"Demo: {self.company_name} ({self.name}) - {self.store_count} stores"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ['-created_at']

    def __str__(self):
        return self.email


class MeetingBooking(models.Model):
    MEETING_FORMAT_CHOICES = [
        ('google_meet', 'Virtual Video Conference (Google Meet)'),
        ('office_harare', 'In-Person (Avail Harare Tech Lab)'),
        ('on_site', 'On-Site Visit (At Your Branch / Store)'),
        ('phone', 'Phone Call / WhatsApp Audio'),
    ]

    TIME_SLOT_CHOICES = [
        ('morning', 'Morning (09:00 - 11:00 CAT)'),
        ('midday', 'Midday (11:00 - 13:00 CAT)'),
        ('afternoon', 'Afternoon (14:00 - 16:00 CAT)'),
        ('late_afternoon', 'Late Afternoon (16:00 - 17:30 CAT)'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company_name = models.CharField(max_length=150)
    meeting_topic = models.CharField(max_length=150, default='Clarity Retail LAN (Motor Spares POS & Offline Edge)')
    meeting_format = models.CharField(max_length=40, choices=MEETING_FORMAT_CHOICES, default='google_meet')
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time_slot = models.CharField(max_length=80, default='Morning (09:00 - 11:00 CAT)')
    store_count = models.CharField(max_length=50, blank=True, default='1')
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Meeting Booking"
        verbose_name_plural = "Meeting Bookings"
        ordering = ['-created_at']

    def __str__(self):
        return f"Meeting: {self.company_name} ({self.name}) - {self.preferred_date} [{self.preferred_time_slot}]"

