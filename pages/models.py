from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category_code = models.CharField(max_length=60, default='01 / ENGINEERING', help_text="e.g. 01 / CUSTOM ENGINEERING")
    short_description = models.TextField(help_text="Short summary for cards and bento grids")
    full_description = models.TextField(blank=True, help_text="Comprehensive service overview")
    icon = models.CharField(max_length=50, default='fa-gears', help_text="FontAwesome icon class")
    deliverables_list = models.TextField(
        blank=True,
        help_text="Newline-separated list of deliverables or features (one bullet per line)"
    )
    turnkey_benefit = models.CharField(max_length=255, blank=True, help_text="Key highlight or ROI summary")
    
    # Service Pricing & Commercial Model (Price Ranges for Professional Services)
    price_min = models.CharField(max_length=50, blank=True, help_text="Minimum price in range, e.g. 1,500, 450, 250")
    price_max = models.CharField(max_length=50, blank=True, help_text="Maximum price in range, e.g. 4,500, 1,200, 850")
    price_amount = models.CharField(max_length=50, default='Custom Quote', blank=True, help_text="Fallback single or base price, e.g. 1,500 – 4,500, Custom Quote")
    billing_period = models.CharField(max_length=60, default='/ SOW milestone', help_text="e.g. / 2-week Sprint, / device model, / store / mo")
    price_min_annual = models.CharField(max_length=50, blank=True, help_text="Discounted annual min, or auto-discounted 20%")
    price_max_annual = models.CharField(max_length=50, blank=True, help_text="Discounted annual max, or auto-discounted 20%")
    price_annual = models.CharField(max_length=50, blank=True, help_text="Annual billing rate or fallback")
    billing_period_annual = models.CharField(max_length=60, default='/ mo, billed annually', blank=True)
    currency_symbol = models.CharField(max_length=10, default='$')
    pricing_model = models.CharField(max_length=120, default='Fixed Milestone or SOW Retainer', help_text="e.g. Scope-Based Milestone SOW, Dedicated Sprint Team, Managed SLA")
    commercial_terms = models.TextField(blank=True, help_text="Newline-separated commercial bullets (e.g. 60-day warranty, Source code escrow)")

    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True, help_text="Show on homepage")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def has_price_range(self):
        return bool(self.price_min and self.price_max)

    @property
    def price_range_display(self):
        """Displays price range e.g. $1,500 – $4,500"""
        if self.price_min and self.price_max:
            return f"{self.currency_symbol}{self.price_min} – {self.currency_symbol}{self.price_max}"
        elif self.price_min:
            return f"From {self.currency_symbol}{self.price_min}"
        elif self.price_amount:
            if '-' in str(self.price_amount) or '–' in str(self.price_amount):
                return f"{self.currency_symbol}{self.price_amount}" if not str(self.price_amount).startswith(self.currency_symbol) else str(self.price_amount)
            return f"{self.currency_symbol}{self.price_amount}"
        return "Custom SOW Scope"

    def get_annual_range_display(self):
        min_ann = self.price_min_annual or self._calc_discount(self.price_min)
        max_ann = self.price_max_annual or self._calc_discount(self.price_max)
        if min_ann and max_ann:
            return f"{self.currency_symbol}{min_ann} – {self.currency_symbol}{max_ann}"
        elif min_ann:
            return f"From {self.currency_symbol}{min_ann}"
        return self.price_range_display

    def _calc_discount(self, val_str):
        if not val_str:
            return ''
        try:
            val = float(str(val_str).replace(',', '').strip())
            return f"{int(round(val * 0.8)):,}"
        except (ValueError, TypeError):
            return str(val_str)

    def get_deliverables(self):
        if not self.deliverables_list:
            return []
        return [line.strip() for line in self.deliverables_list.splitlines() if line.strip()]

    def get_commercial_terms(self):
        if not self.commercial_terms:
            return []
        return [line.strip() for line in self.commercial_terms.splitlines() if line.strip()]

    def get_annual_price(self):
        if self.price_annual:
            return self.price_annual
        if self.price_min and self.price_max:
            return self.get_annual_range_display()
        try:
            val = float(str(self.price_amount).replace(',', '').strip())
            return str(int(round(val * 0.8)))
        except (ValueError, TypeError):
            return self.price_amount



class PricingPlan(models.Model):
    PLAN_TYPES = [
        ('software', 'Software Platform Tier'),
        ('hardware', 'Turnkey Hardware Appliance'),
        ('service', 'Professional Engagement / SLA'),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, default='software')
    tagline = models.CharField(max_length=255, blank=True, help_text="Short description of who it is for")
    price_amount = models.CharField(max_length=50, default='49', help_text="e.g. 49, 149, 450, Custom")
    price_annual = models.CharField(max_length=50, blank=True, help_text="e.g. 39, 119, or auto-discounted 20%")
    billing_period = models.CharField(max_length=50, default='/ store / mo', help_text="e.g. / store / mo, one-off, / chain / mo")
    billing_period_annual = models.CharField(max_length=50, default='/ store / mo, billed annually', blank=True)
    currency_symbol = models.CharField(max_length=10, default='$')

    # Operational scale parameters (Tills, Users, Branches)
    tills_limit = models.CharField(max_length=100, blank=True, help_text="e.g. 1 Till Station, Up to 4 Tills, Unlimited Tills")
    users_limit = models.CharField(max_length=100, blank=True, help_text="e.g. Up to 3 Cashier Users, Up to 10 Users")
    branches_limit = models.CharField(max_length=100, blank=True, help_text="e.g. 1 Store Location, Up to 5 Branches, Enterprise")

    features_list = models.TextField(
        help_text="Newline-separated list of included features/capabilities"
    )
    badge = models.CharField(max_length=60, blank=True, help_text="Optional badge e.g. 'Most Popular', 'Plug & Play'")
    is_featured = models.BooleanField(default=False)
    cta_text = models.CharField(max_length=60, default='Get Started')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def get_annual_price(self):
        if self.price_annual:
            return self.price_annual
        try:
            val = float(str(self.price_amount).replace(',', '').strip())
            return str(int(round(val * 0.8)))
        except (ValueError, TypeError):
            return self.price_amount

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()} - {self.currency_symbol}{self.price_amount})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_features(self):
        if not self.features_list:
            return []
        return [line.strip() for line in self.features_list.splitlines() if line.strip()]


class Capability(models.Model):
    pillar_number = models.CharField(max_length=50, default='Pillar 01', help_text="e.g. Pillar 01, Core Architecture")
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    short_summary = models.TextField(help_text="Teaser summary for bento cards on homepage")
    full_description = models.TextField(blank=True, help_text="Detailed explanation on What We Do page")
    icon = models.CharField(max_length=50, default='fa-server')
    technical_bullets = models.TextField(
        blank=True,
        help_text="Newline-separated technical points"
    )
    key_stat_number = models.CharField(max_length=50, blank=True, help_text="e.g. < 40ms, Zero, 100%")
    key_stat_label = models.CharField(max_length=100, blank=True, help_text="e.g. Edge Scan Latency")
    bento_span = models.PositiveIntegerField(default=8, help_text="Grid column span on homepage (4, 6, 8, or 12)")
    accent_color = models.CharField(max_length=30, default='var(--light-blue)')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Capabilities (What We Do)"
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.pillar_number}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_bullets(self):
        if not self.technical_bullets:
            return []
        return [line.strip() for line in self.technical_bullets.splitlines() if line.strip()]


class FAQItem(models.Model):
    category = models.CharField(max_length=100, default='General', help_text="e.g. Offline Architecture, Hardware, Fiscal")
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"
        ordering = ['order', 'id']

    def __str__(self):
        return self.question


class CompanyMetric(models.Model):
    label = models.CharField(max_length=100, help_text="e.g. Offline Autonomy, Edge Scan Latency")
    value = models.CharField(max_length=50, help_text="e.g. 100%, < 40ms, Sub-Second")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value} - {self.label}"


class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=150, default="Avail Technologies (Pvt) Ltd")
    hero_eyebrow = models.CharField(max_length=100, default="Software Engineering & Digital Infrastructure")
    hero_headline = models.CharField(max_length=255, default="Mission-Critical Software Engineered for African Enterprise")
    hero_subheadline = models.TextField(default="We engineer dependable software systems and custom platforms that automate daily workflows, safeguard critical records, and keep enterprises operating without downtime.")
    vision_statement = models.TextField(
        blank=True,
        default="To be Africa's most trusted software engineering partner, delivering resilient digital platforms that empower companies to operate with complete efficiency, control, and autonomy."
    )
    mission_statement = models.TextField(
        blank=True,
        default="To empower African enterprises with dependable, offline-first software and turnkey systems that eliminate operational bottlenecks, prevent losses, and accelerate growth."
    )
    about_story = models.TextField(
        blank=True,
        default="Founded in 2023, Avail Technologies (Pvt) Ltd engineers practical, high-reliability business software and digital infrastructure. We specialize in operational automation, resilient record keeping, and custom enterprise systems designed to operate without downtime."
    )
    contact_email = models.EmailField(default="info@avail.co.zw")
    contact_phone = models.CharField(max_length=50, default="+263 78 485 1863")
    office_address = models.CharField(max_length=255, default="Harare, Zimbabwe")

    class Meta:
        verbose_name = "Company Profile & Identity"
        verbose_name_plural = "Company Profile & Identity"

    def __str__(self):
        return self.company_name

