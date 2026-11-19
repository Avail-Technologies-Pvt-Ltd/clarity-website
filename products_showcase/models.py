from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-box', help_text="FontAwesome icon class, e.g. fa-cash-register")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Product Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('core_product', 'Core Standalone Product (LAN Appliance)'),
        ('cloud_feature', 'Connected Cloud Feature & Module'),
    ]

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    product_type = models.CharField(
        max_length=40,
        choices=PRODUCT_TYPE_CHOICES,
        default='core_product',
        help_text="The 2 standalone products we sell are Clarity Retail LAN and Clarity Wholesale LAN. Others are features."
    )
    badge = models.CharField(max_length=50, help_text="Badge e.g. 'Offline-First POS', 'Cloud Feature'")
    tagline = models.CharField(max_length=255, help_text="Short one-line pitch")
    description = models.TextField()
    architecture = models.CharField(max_length=100, default='Hybrid Cloud / Local LAN', help_text="e.g. 'Local SQLite/Postgres Engine'")
    
    # Key features stored as newline-separated strings or structured bullets
    features_list = models.TextField(
        help_text="One key feature per line. Format: Title | Description or just bullet point text",
        blank=True
    )
    
    # Specs stored as newline-separated Key: Value
    technical_specs = models.TextField(
        help_text="One technical spec per line. Format: Spec Name: Spec Value",
        blank=True
    )

    icon = models.CharField(max_length=50, default='fa-server')
    logo_image = models.CharField(max_length=255, blank=True, help_text="Static image path or URL for product 3D logo, e.g. images/clarity-retail-logo.png")
    mark_image = models.CharField(max_length=255, blank=True, help_text="Static image path for product emblem mark, e.g. images/clarity-retail-mark.png")
    accent_color = models.CharField(max_length=20, default='#14b8a6', help_text="Hex color code for branding card, e.g. #14b8a6")
    
    # Product Pricing Fields
    price_amount = models.CharField(max_length=50, default='49', help_text="Starting price, e.g. 49, 149, 375, Custom")
    currency_symbol = models.CharField(max_length=10, default='$')
    billing_period = models.CharField(max_length=50, default='/ store / mo', help_text="e.g. / store / mo, / chain / mo, one-off")
    pricing_tagline = models.CharField(max_length=255, blank=True, help_text="e.g. Includes up to 3 POS tills & local database engine")

    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    @property
    def is_standalone_product(self):
        """Returns True if this is one of our 4 commercial products"""
        return True

    @property
    def is_cloud_feature(self):
        return False

    @property
    def access_badge(self):
        return "Core Licensed Product"

    @property
    def access_description(self):
        return self.tagline

    def get_features(self):
        """Returns list of feature dictionaries {title, description}"""
        features = []
        if not self.features_list:
            return features
        for line in self.features_list.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            if '|' in line:
                parts = line.split('|', 1)
                features.append({'title': parts[0].strip(), 'description': parts[1].strip()})
            else:
                features.append({'title': line, 'description': ''})
        return features

    def get_specs(self):
        """Returns list of tuples (name, value)"""
        specs = []
        if not self.technical_specs:
            return specs
        for line in self.technical_specs.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                parts = line.split(':', 1)
                specs.append((parts[0].strip(), parts[1].strip()))
            else:
                specs.append(('Detail', line))
        return specs


class ProductPricingTier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pricing_tiers')
    name = models.CharField(max_length=120, help_text="e.g. Starter Store, Growth Chain, Enterprise Network")
    badge = models.CharField(max_length=60, blank=True, help_text="e.g. 'Most Popular', 'Best Value'")
    tagline = models.CharField(max_length=255, blank=True, help_text="Short description of who this plan fits")
    
    # Pricing fields (Monthly vs Annual)
    price_amount = models.CharField(max_length=50, default='49', help_text="Monthly price, e.g. 49, 149, 375, Custom")
    billing_period = models.CharField(max_length=50, default='/ store / mo', help_text="e.g. / store / mo, / chain / mo, one-off")
    price_annual = models.CharField(max_length=50, blank=True, help_text="Annual price per month or total, e.g. 39, 119, 299 (leave blank to auto-calculate 20% discount)")
    billing_period_annual = models.CharField(max_length=50, default='/ store / mo, billed annually', blank=True)
    
    currency_symbol = models.CharField(max_length=10, default='$')
    
    # Operational scale parameters (Tills, Users, Branches)
    tills_limit = models.CharField(max_length=100, blank=True, help_text="e.g. 1 Till Station, Up to 4 Tills, Unlimited Tills")
    users_limit = models.CharField(max_length=100, blank=True, help_text="e.g. Up to 3 Cashier Users, Up to 10 Cashier/Admin Users")
    branches_limit = models.CharField(max_length=100, blank=True, help_text="e.g. 1 Retail Store, Up to 3 Branches, Multi-Branch Chain")

    features_list = models.TextField(help_text="One included feature per line")
    is_featured = models.BooleanField(default=False)
    cta_text = models.CharField(max_length=60, default='Request Demo / Quote')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.product.name} — {self.name} ({self.currency_symbol}{self.price_amount})"

    def get_annual_price(self):
        """Returns explicitly set price_annual or calculates 20% discount if numeric"""
        if self.price_annual:
            return self.price_annual
        try:
            val = float(str(self.price_amount).replace(',', '').strip())
            # 20% annual discount rounded
            discounted = int(round(val * 0.8))
            return str(discounted)
        except (ValueError, TypeError):
            return self.price_amount

    def get_features(self):
        if not self.features_list:
            return []
        return [line.strip() for line in self.features_list.splitlines() if line.strip()]


class ProductInstruction(models.Model):
    """
    Platform User Manual Chapter & Operational Guide
    Contains searchable procedures, step-by-step how-tos, configuration notes, and critical warnings.
    """
    MANUAL_TYPES = [
        ('user_guide', 'End-User / Cashier Operations Guide'),
        ('admin_manual', 'Branch Supervisor & Admin Manual'),
        ('setup_guide', 'Hardware Setup & Installation Manual'),
        ('troubleshoot', 'Diagnostics & Troubleshooting Protocol'),
        ('warning_protocol', 'Statutory Fiscal & Critical Warning'),
    ]

    SEVERITY_LEVELS = [
        ('info', 'Standard Operation / Guide'),
        ('caution', 'Caution / Best Practice'),
        ('warning', 'Operational Warning (Risk of Data/Inventory Loss)'),
        ('critical', 'Critical Statutory / Fiscal Compliance Hazard'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='instructions')
    section_number = models.CharField(max_length=20, default='1.0', help_text="e.g. 1.0, 2.1, 4.3 (Manual chapter sequence)")
    title = models.CharField(max_length=200, help_text="e.g. Daily Cashier Float In & Blind Cash Drops")
    slug = models.SlugField(max_length=200, blank=True)
    instruction_type = models.CharField(max_length=25, choices=MANUAL_TYPES, default='user_guide', verbose_name="Manual Category")
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='info', help_text="Visual badge and alert styling")
    category = models.CharField(max_length=100, default='Core Operations', help_text="Manual Chapter, e.g. Till Operations, Fiscal ESD, Printer Setup, End-of-Day")
    
    summary = models.TextField(help_text="Executive summary of this manual chapter / procedure")
    
    # Detailed comprehensive manual content (rich text / markdown paragraphs)
    detailed_content = models.TextField(
        blank=True,
        help_text="Comprehensive user manual documentation, explanations, and edge-case behavior"
    )

    # Step-by-step how-to instructions
    steps_list = models.TextField(
        help_text="Numbered operational steps (one per line). e.g. Step 1: Open Till Management screen...",
        blank=True
    )
    
    # Prominent Warnings or Caution Notes
    warning_notes = models.TextField(
        blank=True,
        help_text="Critical statutory or operational warnings. e.g. Never power off ESD device mid-fiscalisation"
    )
    
    # Configuration / Code / Keyboard shortcuts
    code_snippet = models.TextField(
        blank=True,
        help_text="Optional configuration keys, CLI commands, or shortcut table"
    )
    
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated search tags, e.g. float, refund, void, printer, usb, z-report")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Platform User Manual Topic"
        verbose_name_plural = "Platform User Manual Topics"
        ordering = ['order', 'section_number', 'title']

    def __str__(self):
        return f"[{self.product.name}] §{self.section_number} {self.title}"

    def get_steps(self):
        if not self.steps_list:
            return []
        return [line.strip() for line in self.steps_list.splitlines() if line.strip()]


class HardwareProduct(models.Model):
    name = models.CharField(max_length=150, help_text="e.g. POS Thermal Receipt Printers, Commercial A4 Printers")
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    hardware_category = models.CharField(
        max_length=100,
        default='POS Peripherals',
        help_text="e.g. POS Printers, A4 Printers, Barcode Readers, Laptops, Network Infrastructure"
    )
    tagline = models.CharField(max_length=255, help_text="Short highlight, e.g. High-speed 80mm thermal printing with auto-cutter")
    description = models.TextField(help_text="Full product overview and role in retail/enterprise environments")
    icon = models.CharField(max_length=50, default='fa-print', help_text="FontAwesome icon class")
    
    # Specs & Deliverables
    specs_list = models.TextField(
        blank=True,
        help_text="Newline-separated list of hardware specifications"
    )
    key_features = models.TextField(
        blank=True,
        help_text="Newline-separated key features or compatibility notes"
    )
    
    # Commercial Pricing Range (Per unit or staging kit)
    price_min = models.CharField(max_length=50, blank=True, help_text="Minimum price, e.g. 120, 350, 450")
    price_max = models.CharField(max_length=50, blank=True, help_text="Maximum price, e.g. 180, 600, 750")
    price_unit = models.CharField(max_length=60, default='/ unit', help_text="e.g. / unit, / kit, / meter spool")
    currency_symbol = models.CharField(max_length=10, default='$')
    warranty = models.CharField(max_length=100, default='12-Month Hardware Replacement Warranty')
    badge = models.CharField(max_length=50, default='Turnkey Certified', blank=True)
    
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hardware Product"
        verbose_name_plural = "Hardware Products"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.hardware_category})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:hardware_detail', kwargs={'slug': self.slug})

    @property
    def price_range_display(self):
        if self.price_min and self.price_max:
            return f"{self.currency_symbol}{self.price_min} – {self.currency_symbol}{self.price_max}"
        elif self.price_min:
            return f"From {self.currency_symbol}{self.price_min}"
        return "Quote on Request"

    @property
    def image_static_path(self):
        return f"images/hardware/{self.slug}.webp"

    @property
    def image_jpg_path(self):
        return f"images/hardware/{self.slug}.jpg"

    def get_specs(self):
        specs = []
        if not self.specs_list:
            return specs
        for line in self.specs_list.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                parts = line.split(':', 1)
                specs.append((parts[0].strip(), parts[1].strip()))
            else:
                specs.append(('Specification', line))
        return specs

    def get_features(self):
        if not self.key_features:
            return []
        return [line.strip() for line in self.key_features.splitlines() if line.strip()]



