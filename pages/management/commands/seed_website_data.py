import os
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from pages.models import Capability, Service, PricingPlan, FAQItem, CompanyMetric, CompanyProfile
from products_showcase.models import ProductCategory, Product, ProductPricingTier, HardwareProduct, ProductInstruction
from blog.models import Category as BlogCategory, Post
from seed_manuals import seed_manuals_data

class Command(BaseCommand):
    help = "Seeds initial production data for Avail Technologies website (Clean 4 Core LANs/Products, no Hubs)"

    def handle(self, *args, **options):
        self.stdout.write("Seeding website production data...")

        # ── 1. Company Profile ─────────────────────────────────────────────────
        CompanyProfile.objects.update_or_create(
            id=1,
            defaults={
                'company_name': 'Avail Technologies (Pvt) Ltd',
                'hero_eyebrow': 'Smart Business Software & Retail Solutions',
                'hero_headline': 'Practical Business Software Built for African Retail',
                'hero_subheadline': 'Speed up counter sales, take multi-currency payments, track stock across branches, and stay 100% tax compliant—even during power and internet cuts.',
                'vision_statement': "To be Africa's most trusted business technology partner, where every solution we deliver empowers companies to operate with complete efficiency, control, and profitability.",
                'mission_statement': 'To empower African businesses with practical, dependable software and turnkey hardware that eliminates counter delays, prevents stock losses, and accelerates growth, delivered with client-first dedication.',
                'about_story': 'Founded in 2023, Avail Technologies Pvt Ltd crafts practical, reliable business software that eliminates operational bottlenecks for retailers, wholesalers, and modern African enterprises.',
                'contact_email': 'info@avail.co.zw',
                'contact_phone': '+263 78 485 1863',
                'office_address': 'Harare, Zimbabwe',
            }
        )
        self.stdout.write("  [OK] Company Profile seeded")

        # ── 2. Capabilities (Bento Pillars) ────────────────────────────────────
        capabilities_data = [
            {
                'pillar_number': 'Pillar 01',
                'title': '100% Uninterrupted Store & Counter Operations',
                'slug': 'edge-systems',
                'short_summary': 'Your cashiers keep ringing sales, scanning barcodes, and printing receipts even when the internet goes down or the power grid flickers.',
                'full_description': (
                    "Power outages and internet dropouts should never cost you a customer or stop a sale. We equip your stores with autonomous counter systems that run continuously without relying on an active internet connection.\n\n"
                    "Cashiers ring sales instantly, look up spare parts or barcodes in milliseconds, and print receipts smoothly. The moment internet is back, all daily sales and stock movements automatically synchronize to your central management dashboard."
                ),
                'icon': 'fa-cash-register',
                'technical_bullets': (
                    "Fast barcode and part number search at checkout\n"
                    "Zero downtime during internet or network outages\n"
                    "Automatic background sync when connectivity restores\n"
                    "Complete shift audit and secure till cash reconciliation"
                ),
                'key_stat_number': '100%',
                'key_stat_label': 'Store Sales Uptime',
                'bento_span': 8,
                'order': 1,
            },
            {
                'pillar_number': 'Pillar 02',
                'title': 'Certified ZIMRA Fiscal & Tax Compliance',
                'slug': 'fiscal-engineering',
                'short_summary': 'Direct connection to certified Electronic Signature Devices (ESD) and fiscal printers for fast, legally verified receipts and QR codes.',
                'full_description': (
                    "Complying with statutory fiscalisation laws shouldn't slow down your checkout lines or cause compliance headaches. Our software connects directly to certified tax fiscal devices and signature units.\n\n"
                    "Every customer sale is instantly signed with official QR codes and statutory codes, keeping your business fully compliant with revenue authority regulations without any cashier delays."
                ),
                'icon': 'fa-receipt',
                'technical_bullets': (
                    "Certified ZIMRA Fiscal Device Integration\n"
                    "Instant QR Code Verification on Every Receipt\n"
                    "Dual-Currency USD and ZiG Tax Invoicing\n"
                    "Automated Daily Fiscal Z-Reports & Audits"
                ),
                'key_stat_number': '100%',
                'key_stat_label': 'Tax & Fiscal Compliance',
                'bento_span': 4,
                'order': 2,
            },
            {
                'pillar_number': 'Pillar 03',
                'title': 'Turnkey POS Equipment & Hardware Kits',
                'slug': 'hardware-staging',
                'short_summary': 'Ready-to-use till workstations, heavy-duty thermal receipt printers, optical barcode scanners, and cash drawers delivered and installed on day one.',
                'full_description': (
                    "Setting up a new till or opening a branch shouldn't involve hunting for compatible cables and drivers. We supply complete, pre-configured hardware kits tailored to high-volume retail.\n\n"
                    "Every unit is thoroughly tested before delivery so your staff can start serving customers immediately with zero technical setup hassle."
                ),
                'icon': 'fa-desktop',
                'technical_bullets': (
                    "Complete plug-and-play counter workstations\n"
                    "Heavy-duty 80mm thermal receipt printers & cash drawers\n"
                    "Fast optical handheld and hands-free 2D barcode scanners\n"
                    "On-site installation, cabling, and staff orientation"
                ),
                'key_stat_number': '< 2 Hrs',
                'key_stat_label': 'Average Till Setup Time',
                'bento_span': 4,
                'order': 3,
            },
            {
                'pillar_number': 'Pillar 04',
                'title': 'Dedicated Business Support & Maintenance',
                'slug': 'managed-operations',
                'short_summary': 'Responsive support hotline, daily secure cloud backups, on-site assistance, and staff refresher training to keep your operations running smoothly.',
                'full_description': (
                    "Retail shops, motor spares counters, and wholesale depots cannot afford delays during morning rushes or weekend shopping peaks. Our dedicated support team is always on call.\n\n"
                    "We monitor system health, safeguard your sales records with automated off-site backups, and provide fast assistance via WhatsApp and on-site visits."
                ),
                'icon': 'fa-shield-halved',
                'technical_bullets': (
                    "Quick response time via dedicated WhatsApp & phone\n"
                    "Automated daily secure cloud backups\n"
                    "Regular system health checks & preventative care\n"
                    "Staff onboarding & cashier refresher training"
                ),
                'key_stat_number': '99.4%',
                'key_stat_label': 'Client Satisfaction Rate',
                'bento_span': 8,
                'order': 4,
            },
        ]
        for cap in capabilities_data:
            Capability.objects.update_or_create(slug=cap['slug'], defaults=cap)
        self.stdout.write("  [OK] Capabilities seeded")

        # ── 3. Services ────────────────────────────────────────────────────────
        services_data = [
            {
                'title': 'Custom Business Software & ERP Integration',
                'slug': 'custom-engineering',
                'category_code': '01 / BUSINESS SOFTWARE',
                'short_description': 'Tailored point-of-sale features, multi-currency accounting logic, warehouse dispatches, and seamless data migration from Excel, Pastel, or QuickBooks.',
                'full_description': 'Every retail chain has unique operational requirements that off-the-shelf software cannot satisfy. We deliver tailored software solutions that fit your business model perfectly.',
                'icon': 'fa-laptop-code',
                'deliverables_list': (
                    "Custom Point-of-Sale Checkout Workflows\n"
                    "Multi-Currency Cash Drawer Reconciliation (USD & ZiG)\n"
                    "Warehouse Bin-Location Picking & Packing\n"
                    "Legacy System Data Migration (Pastel, QuickBooks, Excel)"
                ),
                'turnkey_benefit': 'Software built around your exact business workflow rather than forcing your business to adapt.',
                'price_amount': 'Custom',
                'currency_symbol': '',
                'billing_period': 'milestone-based',
                'pricing_model': 'Custom Project Scope',
                'commercial_terms': (
                    "Comprehensive on-site operational discovery phase\n"
                    "Clear deliverables and milestone-based sign-offs\n"
                    "User Acceptance Testing (UAT) staff training\n"
                    "Post-launch warranty & ongoing technical assistance"
                ),
                'order': 1,
                'is_featured': True,
            },
            {
                'title': 'Turnkey POS Hardware Kits & Setup',
                'slug': 'hardware-staging-service',
                'category_code': '02 / POS HARDWARE',
                'short_description': 'Pre-configured till workstations, thermal receipt printers, optical barcode scanners, and cash drawers delivered ready to trade.',
                'full_description': 'Setting up retail checkout counters shouldn’t require weeks of troubleshooting. We supply complete turnkey hardware kits ready for immediate commercial trade.',
                'icon': 'fa-desktop',
                'deliverables_list': (
                    "Ready-to-Trade Store Counter Workstations\n"
                    "High-Speed Thermal Receipt Printers & Heavy-Duty Cash Drawers\n"
                    "Fast Optical Barcode Label Printers & Scanners\n"
                    "On-Site Cabling & Complete Counter Testing"
                ),
                'turnkey_benefit': 'Plug into the wall, connect the till monitors, and start ringing sales in under two hours.',
                'price_amount': '450',
                'currency_symbol': '$',
                'billing_period': 'one-off appliance kit',
                'pricing_model': 'Ready-to-Trade Hardware Bundle',
                'commercial_terms': (
                    "Pre-installed and fully configured for immediate use\n"
                    "Thoroughly quality-tested before delivery\n"
                    "Built-in battery backup for power load shedding\n"
                    "Hardware replacement warranty and setup support"
                ),
                'order': 2,
                'is_featured': True,
            },
            {
                'title': 'ZIMRA Fiscal Device Setup & Compliance',
                'slug': 'fiscal-integration',
                'category_code': '03 / FISCAL COMPLIANCE',
                'short_description': 'Certified connection to Electronic Signature Devices (ESD), fiscal printers, and automated tax authority synchronization.',
                'full_description': 'Navigating governmental tax compliance regulations can stall retail rollouts. We provide certified fiscal device integration, driver configuration, and tax authority synchronization.',
                'icon': 'fa-file-invoice-dollar',
                'deliverables_list': (
                    "Certified Electronic Signature Device (ESD) Integration\n"
                    "Automated QR Code Signing & Daily Z-Reports\n"
                    "Compliant Dual-Currency Invoicing (USD & ZiG)\n"
                    "Statutory Fiscal Memory Auditing & Reporting"
                ),
                'turnkey_benefit': '100% compliant with local statutory revenue authority requirements with zero checkout slowdowns.',
                'price_amount': '250',
                'currency_symbol': '$',
                'billing_period': 'per device model',
                'pricing_model': 'Fiscal Setup & Certification',
                'commercial_terms': (
                    "Certified Electronic Signature Device (ESD) connection\n"
                    "Official revenue authority compliance verification\n"
                    "Instant QR code receipt generation on every sale\n"
                    "Automated statutory daily Z-report printing"
                ),
                'order': 3,
                'is_featured': True,
            },
            {
                'title': 'Dedicated Store Support & Maintenance',
                'slug': 'managed-operations-service',
                'category_code': '04 / STORE SUPPORT',
                'short_description': 'Proactive system monitoring, daily off-site cloud backups, dedicated WhatsApp emergency hotline, and on-site technician dispatch.',
                'full_description': 'Retail shops and distribution hubs cannot afford downtime during peak shopping hours or weekend rushes. Our support agreements provide peace of mind and rapid response.',
                'icon': 'fa-shield-halved',
                'deliverables_list': (
                    "Rapid Critical Incident Response Time\n"
                    "Continuous Store System Monitoring\n"
                    "Automated Daily Off-Site Cloud Backups\n"
                    "Dedicated WhatsApp Hotline & Technician Dispatch"
                ),
                'turnkey_benefit': 'Guaranteed response times, secure data backups, and peace of mind for your business.',
                'price_amount': '150',
                'currency_symbol': '$',
                'billing_period': '/ store / mo',
                'pricing_model': 'Monthly Store Maintenance Plan',
                'commercial_terms': (
                    "Priority assistance via WhatsApp and direct telephone\n"
                    "Automated daily encrypted off-site cloud backups\n"
                    "Regular system health checks & data optimization\n"
                    "Staff refresher training and on-site technician support"
                ),
                'order': 4,
                'is_featured': True,
            },
        ]
        for s in services_data:
            Service.objects.update_or_create(slug=s['slug'], defaults=s)
        self.stdout.write("  [OK] Services seeded")

        # ── 4. Pricing Plans ───────────────────────────────────────────────────
        pricing_data = [
            # Software Plans (LAN Systems)
            {
                'name': 'Single-Till Retail LAN',
                'slug': 'single-till-retail-lan',
                'plan_type': 'software',
                'tagline': 'Single independent retail shop, spares counter, or boutique storefront.',
                'price_amount': '30',
                'currency_symbol': '$',
                'billing_period': '/ store / mo',
                'features_list': (
                    "1 Store Location\n"
                    "1 Dedicated Counter Sales Till\n"
                    "Up to 3 Cashier & Supervisor Accounts\n"
                    "100% Offline Checkout with Zero Internet Dependency\n"
                    "Dual-Currency (USD & ZiG) Cash Register\n"
                    "Certified Fiscal Device Direct USB Driver\n"
                    "Automated Encrypted Daily Local Backup\n"
                    "Standard Business-Hours Support"
                ),
                'badge': 'Starter Counter',
                'is_featured': False,
                'cta_text': 'Get Started',
                'order': 1,
            },
            {
                'name': 'Multi-Till Retail Store',
                'slug': 'multi-till-retail-store',
                'plan_type': 'software',
                'tagline': 'Bustling retail supermarket, spares store, or multi-till checkout floor.',
                'price_amount': '59',
                'currency_symbol': '$',
                'billing_period': '/ store / mo',
                'features_list': (
                    "1 Store Location (Expandable)\n"
                    "Up to 4 Concurrent Till Lanes on Local LAN\n"
                    "Up to 10 Cashier & Staff Accounts\n"
                    "Instant Peer-to-Peer LAN Synchronization\n"
                    "Supervisor Overrides & Blind Cash Drops\n"
                    "Integrated Thermal Receipt & Barcode Scale Drivers\n"
                    "Priority WhatsApp SLA & Phone Support"
                ),
                'badge': 'Most Popular',
                'is_featured': True,
                'cta_text': 'Select Multi-Till Plan',
                'order': 2,
            },
            {
                'name': 'Wholesale Depot LAN',
                'slug': 'wholesale-depot-lan',
                'plan_type': 'software',
                'tagline': 'High-volume auto parts bulk inventory, carton breakdowns, and trade dispatches.',
                'price_amount': '149',
                'currency_symbol': '$',
                'billing_period': '/ depot / mo',
                'features_list': (
                    "1 Wholesale Depot Facility\n"
                    "Up to 3 Invoicing Desks Included\n"
                    "Up to 8 Staff & Sales Accounts\n"
                    "Multi-Tier Packaging Units (Piece -> Pack -> Carton)\n"
                    "Customer Credit Ledger & Debtor Statements\n"
                    "Loading Bay Gate Pass Verification\n"
                    "Priority Business Support & Setup"
                ),
                'badge': 'Depot Starter',
                'is_featured': False,
                'cta_text': 'Select Wholesale Depot',
                'order': 3,
            },
            {
                'name': 'Enterprise & Multi-Branch LAN',
                'slug': 'enterprise-multi-branch-lan',
                'plan_type': 'software',
                'tagline': 'Multi-branch retail chains and nationwide wholesale distribution networks.',
                'price_amount': '375',
                'currency_symbol': '$',
                'billing_period': '/ network / mo',
                'features_list': (
                    "Multi-Branch Retail or Depot Network\n"
                    "Unlimited Concurrent Till Stations\n"
                    "Unlimited Staff Accounts\n"
                    "Cross-Branch Inventory Sync & Price Pushes\n"
                    "Custom ERP Integration & Automated Backups\n"
                    "24/7 Priority Support & Dedicated Account Manager"
                ),
                'badge': 'Enterprise Scale',
                'is_featured': False,
                'cta_text': 'Contact Enterprise',
                'order': 4,
            },
            # Hardware
            {
                'name': 'Store Server Appliance',
                'slug': 'store-server-appliance',
                'plan_type': 'hardware',
                'tagline': 'Heavy-duty store counter server with battery backup, pre-configured and ready to trade.',
                'price_amount': '450',
                'currency_symbol': '$',
                'billing_period': 'one-off appliance',
                'features_list': (
                    "Pre-Configured & Ready to Plug In\n"
                    "Handles up to 30 concurrent Till Lanes\n"
                    "Built-in Battery Backup for Load Shedding\n"
                    "3-Year Hardware Replacement Warranty"
                ),
                'badge': 'Plug & Play',
                'is_featured': False,
                'cta_text': 'Order Hardware',
                'order': 5,
            },
            {
                'name': 'Touch POS Till Station',
                'slug': 'touch-pos-till-station',
                'plan_type': 'hardware',
                'tagline': 'Capacitive multi-touch 15.6" POS workstation paired with 80mm thermal printer.',
                'price_amount': '550',
                'currency_symbol': '$',
                'billing_period': 'per lane kit',
                'features_list': (
                    "High-Speed ESC/POS Thermal Receipt Printer\n"
                    "Heavy-Duty Steel 5-Note Cash Drawer\n"
                    "Hands-Free 2D Laser Barcode Scanner\n"
                    "Sturdy Ergonomic Metal Counter Stand"
                ),
                'badge': 'Complete Lane',
                'is_featured': False,
                'cta_text': 'Order Hardware',
                'order': 6,
            },
            {
                'name': 'Fiscal Device Integration Kit',
                'slug': 'fiscal-integration-kit',
                'plan_type': 'hardware',
                'tagline': 'Certified Electronic Signature Device (ESD) or Fiscal Memory Unit.',
                'price_amount': '320',
                'currency_symbol': '$',
                'billing_period': 'certified unit',
                'features_list': (
                    "Compliant with Statutory Revenue Authority Codes\n"
                    "Real-time QR Code Signature Verification\n"
                    "Device Registration & Driver Setup Included\n"
                    "Tamper-Evident Fiscal Memory Casing"
                ),
                'badge': 'Tax Certified',
                'is_featured': False,
                'cta_text': 'Order Hardware',
                'order': 7,
            },
        ]
        for p in pricing_data:
            PricingPlan.objects.update_or_create(slug=p['slug'], defaults=p)
        self.stdout.write("  [OK] Pricing plans seeded")

        # ── 5. Product Categories & Core Software Products ─────────────────────
        cat_retail, _ = ProductCategory.objects.get_or_create(
            slug='motor-spares-retail',
            defaults={
                'name': 'Motor Spares & Auto Retail',
                'description': 'Counter POS, part lookups, and local shop inventory.',
                'icon': 'fa-car',
                'order': 1,
            }
        )

        cat_wholesale, _ = ProductCategory.objects.get_or_create(
            slug='motor-spares-wholesale',
            defaults={
                'name': 'Motor Spares Wholesale & Importers',
                'description': 'Bulk parts receiving, mechanic price lists, and trade accounts.',
                'icon': 'fa-truck-ramp-box',
                'order': 2,
            }
        )

        cat_hostel, _ = ProductCategory.objects.get_or_create(
            slug='hostel-management',
            defaults={
                'name': 'Student Hostels & Accommodation',
                'description': 'Bed allocations, student rent tracking, and maintenance logs.',
                'icon': 'fa-bed',
                'order': 3,
            }
        )

        cat_event, _ = ProductCategory.objects.get_or_create(
            slug='event-management',
            defaults={
                'name': 'Events & Conferences',
                'description': 'Sub-second QR gate scanning, ticket sales, and badge printing.',
                'icon': 'fa-calendar-check',
                'order': 4,
            }
        )

        # Strictly the 4 commercial software products (NO Hubs)
        products_data = [
            {
                'category': cat_retail,
                'name': 'Clarity Retail LAN',
                'slug': 'clarity-retail-lan',
                'product_type': 'core_product',
                'badge': 'Offline-Ready Store POS',
                'tagline': 'Fast touch point-of-sale and in-store counter system that never stops during internet or power cuts.',
                'description': (
                    "Clarity Retail LAN is designed for motor spares shops, auto parts retailers, hardware merchants, and supermarkets. It eliminates checkout queues and keeps your business selling smoothly, even when internet or mobile networks are completely offline.\n\n"
                    "Enjoy instant barcode lookups, multi-currency cash and electronic payment splits, cash drawer controls, and certified ZIMRA fiscal receipts."
                ),
                'architecture': 'Offline-Ready In-Store Counter System with Cloud Sync',
                'features_list': (
                    "Auto Parts & Vehicle Compatibility Engine | Cashiers can search by part description, OEM code, or barcode, or select a vehicle make, model, and transmission to view all compatible spares in stock. You can also map new vehicle compatibility directly from the counter.\n"
                    "100% Offline Checkout Autonomy | Operates fully offline on your store counter server. Ring up sales, calculate live exchange rates between USD and ZiG, split single payments across cash, swipe, and mobile money, and reprint transaction receipts in one click.\n"
                    "Built-in Quotation & Pro-Forma Sales Suite | Counter salesmen can save an active customer basket as a formal quotation. When the customer returns, recall the quotation, verify live stock availability, and copy all items straight into the cart for instant checkout.\n"
                    "Certified ZIMRA Fiscal Device Integration | Fully integrated with certified Electronic Signature Devices (ESD) and fiscal printers. Generates compliant fiscal receipts. During network cuts, receipts are held securely in a local queue and automatically submitted when connection restores.\n"
                    "Direct Thermal Print Server & RJ11 Drawer Kick | Powered by a dedicated background print service that communicates directly with your 80mm thermal receipt printers. Eliminates browser print dialog popups, cuts paper cleanly, and automatically triggers the cash drawer kick.\n"
                    "Inter-Branch Transfers & Multi-Batch Inventory | Move inventory between retail branches with multi-item stock transfer manifests and receipt confirmations. Track batches with individual cost prices, profit markups, and supplier receiving invoices (GRN)."
                ),
                'minor_features': (
                    "Counter & Cashier: Sub-second parts lookup by OEM code, barcode, or description\n"
                    "Counter & Cashier: Vehicle compatibility search matching spares to car make, model, and transmission\n"
                    "Counter & Cashier: Live stock availability indicators directly on checkout screen\n"
                    "Counter & Cashier: Multi-tender split payments (USD cash, ZiG, swipe card, mobile money)\n"
                    "Counter & Cashier: Save active cart as a formal quotation with custom pricing\n"
                    "Counter & Cashier: One-click copy of approved quotation into checkout cart\n"
                    "Counter & Cashier: Live quotation stock availability check before final payment\n"
                    "Counter & Cashier: Quick-reprint of last cashier receipt with zero search delay\n"
                    "Counter & Cashier: Line-item deletion, price adjustment, and full cart voiding controls\n"
                    "Counter & Cashier: Petty cash payout and cash-in vouchers for store expense tracking\n"
                    "Parts & Inventory: Multi-batch inventory tracking with individual cost prices and markups\n"
                    "Parts & Inventory: Supplier Goods Receiving Invoices (GRN) with landed cost records\n"
                    "Parts & Inventory: Customer returns inwards and supplier returns outwards with audit reasons\n"
                    "Parts & Inventory: Credit notes and temporary invoicing modules\n"
                    "Parts & Inventory: Inter-branch stock transfer manifests with dispatch and receipt confirmations\n"
                    "Parts & Inventory: Thermal barcode label and shelf price tag designer with custom templates\n"
                    "Parts & Inventory: Batch stock adjustments with mandatory audit reason logging\n"
                    "Parts & Inventory: Add and map new vehicle models and compatibility directly from the counter\n"
                    "Reports & Analytics: Day-end, Month-end, and Year-end summary reports printed directly to thermal till\n"
                    "Reports & Analytics: Daily transaction breakdown with invoice-by-invoice audit trails\n"
                    "Reports & Analytics: Automated purchasing recommendations based on stock velocity and depletion\n"
                    "Reports & Analytics: Comparative stock movement and periodic inventory turnover reports\n"
                    "Finance & Equity: Store operational expense logging by custom expense categories\n"
                    "Finance & Equity: Cash withdrawals tracking with manager authorization notes\n"
                    "Finance & Equity: Investor equity ledgers, dividend declarations, and payout allocations\n"
                    "System & Hardware: Dedicated background Windows print server with zero browser popups\n"
                    "System & Hardware: Automated receipt cutting and RJ11 pulse trigger to open cash drawer\n"
                    "System & Hardware: Offline ZIMRA fiscal sync queue buffering receipts during network cuts\n"
                    "System & Hardware: One-click local database backup and modal-guided restore suite\n"
                    "System & Hardware: Edge cloud sync client connecting local branch to central Clarity Retail Hub"
                ),
                'technical_specs': (
                    "Target Business: Motor Spares Retailers, Auto Parts Shops, Hardware Stores, Supermarkets\n"
                    "Operation Mode: 100% Offline Checkout with Auto Cloud Sync\n"
                    "Currency Support: Dual-Currency (USD, ZiG, Split Cash & Mobile/Card Payments)\n"
                    "Tax Compliance: Certified ZIMRA Fiscal Device & Receipt Printing\n"
                    "Hardware Compatibility: Standard PC/Laptops, Touch Tills, 80mm Thermal & A4 Printers"
                ),
                'icon': 'fa-cash-register',
                'logo_image': 'images/clarity-retail-logo.png',
                'mark_image': 'images/clarity-retail-mark.png',
                'accent_color': 'var(--light-blue)',
                'price_amount': '30',
                'currency_symbol': '$',
                'billing_period': '/ store / mo',
                'pricing_tagline': 'Starts at $30/mo for 1 till station with 15% annual savings',
                'is_featured': True,
                'order': 1,
            },
            {
                'category': cat_wholesale,
                'name': 'Clarity Wholesale LAN',
                'slug': 'clarity-wholesale-lan',
                'product_type': 'core_product',
                'badge': 'Wholesale & Depot Manager',
                'tagline': 'Bulk inventory management, trade price tiers, container receiving, and secure gate dispatches.',
                'description': (
                    "Built specifically for motor spares wholesale depots, automotive parts importers, and fleet distribution centers.\n\n"
                    "Clarity Wholesale LAN supports mechanic price lists, container receiving, carton breakdowns, debtor credit limits, and loading bay gate passes."
                ),
                'architecture': 'Depot Inventory & Dispatch Management System',
                'features_list': (
                    "Multi-Tier Packaging Units | Automatic unit conversions when breaking bulk containers into trade packs and individual pieces without manual stock adjustment.\n"
                    "Debtor Credit Limits & Aging Ledger | Real-time tracking of debtor balances, payment terms (7, 14, 30 days), automatic credit hold stops, and printable account statements.\n"
                    "Loading Bay Picking & Verification | Separation of commercial invoicing from warehouse picking slips, ensuring pickers only pack verified invoice lines.\n"
                    "Gate Pass Security Verification | Generates scannable dispatch gate passes verified by security personnel before transport trucks exit the depot."
                ),
                'minor_features': (
                    "Depot Operations: Container receiving module with landed cost allocation\n"
                    "Depot Operations: Multi-warehouse transfer notes and branch replenishment requests\n"
                    "Depot Operations: Fast bulk invoice printing in A4 and continuous feed voucher formats\n"
                    "Depot Operations: Pro-forma invoice and commercial quotation generation\n"
                    "Depot Operations: Trade customer price tiers (Mechanic, Reseller, Government, Fleet)\n"
                    "Dispatch & Logistics: Loading bay queue tracking and picker performance monitoring\n"
                    "Dispatch & Logistics: Scannable barcode gate passes for delivery trucks and couriers\n"
                    "Dispatch & Logistics: Return to vendor (RTV) and defective warranty claim tracking\n"
                    "Finance & Credit: Automated debtor aging analysis (Current, 30, 60, 90+ days)\n"
                    "Finance & Credit: Credit stop overrides requiring managing director digital sign-off\n"
                    "Finance & Credit: Multiple price matrix per customer account\n"
                    "Security: Comprehensive audit trail logging every stock adjustment and credit note"
                ),
                'technical_specs': (
                    "Target Business: Auto Parts Wholesalers, Importers & Distribution Depots\n"
                    "Packaging Units: Sell by Piece, Pack, Carton, or Pallet with Auto-Conversion\n"
                    "Credit Management: Real-Time Debtor Ledgers, Aging Balances & Credit Locks\n"
                    "Dispatch Security: Barcode-Verified Picking Lists & Gate Passes"
                ),
                'icon': 'fa-warehouse',
                'logo_image': 'images/clarity-wholesale-logo.png',
                'mark_image': 'images/clarity-wholesale-mark.png',
                'accent_color': 'var(--light-blue)',
                'price_amount': '89',
                'currency_symbol': '$',
                'billing_period': '/ depot / mo',
                'pricing_tagline': 'Bulk packaging units, debtor credit management & loading gate passes',
                'is_featured': True,
                'order': 2,
            },
            {
                'category': cat_hostel,
                'name': 'Hostel Management System',
                'slug': 'hostel-management-system',
                'product_type': 'core_product',
                'badge': 'Hostel & Dorm Manager',
                'tagline': 'Effortless student room allocations, rent payment tracking, and resident directory.',
                'description': (
                    "An intuitive and reliable management platform designed specifically for private student hostels, university dorms, and residential complexes.\n\n"
                    "Manage room assignments, student leases, installment payment plans, maintenance tickets, and check-in rosters effortlessly."
                ),
                'architecture': 'Online Student Accommodation & Rent Management Portal',
                'features_list': (
                    "Visual Room & Bed Allocator | Color-coded visual floor maps showing vacant, occupied, reserved, and maintenance-blocked beds across all room wings.\n"
                    "Student Rent & Deposit Ledger | Automatic rent invoices, damage deposit records, installment payment schedules, and instant printable receipts.\n"
                    "Maintenance Ticket Workflow | Students and wardens log repair tickets (plumbing, electrical, room furniture) with status tracking through to resolution.\n"
                    "Gate Access & Resident Directory | Searchable student rosters with parent/guardian contact numbers, university program details, and photo identification."
                ),
                'minor_features': (
                    "Resident Management: Student lease agreement generation and digital signature capture\n"
                    "Resident Management: Room check-in and check-out inventory condition inspection sheets\n"
                    "Resident Management: Overnight guest registration and visitor log\n"
                    "Resident Management: Emergency contact directory accessible by hostel security 24/7\n"
                    "Billing & Rent: Multi-term rent payment plans (Semester upfront, Monthly installments)\n"
                    "Billing & Rent: Security deposit refund calculator accounting for room repair deductions\n"
                    "Billing & Rent: Automated SMS rent balance reminders to students and sponsors\n"
                    "Operations: Facility asset register tracking beds, mattresses, study desks, and geysers\n"
                    "Operations: Warden daily inspection logs and curfew attendance register\n"
                    "Operations: Separate portal logins for warden, administrator, and property owner"
                ),
                'technical_specs': (
                    "Facility Types: Private Student Hostels, University Dorms & Boarding Houses\n"
                    "Capacity: Scales from 20 to 2,000+ Resident Beds\n"
                    "Rent Tracking: Digital Rent Receipts, Payment Balances & SMS Alerts\n"
                    "Access Controls: Separate Logins for Warden, Accountant & Administrator"
                ),
                'icon': 'fa-bed',
                'logo_image': '',
                'mark_image': '',
                'accent_color': 'var(--color-gold)',
                'price_amount': '30',
                'currency_symbol': '$',
                'billing_period': '/ hostel / mo',
                'pricing_tagline': 'Complete room allocation, rent ledger & resident management',
                'is_featured': True,
                'order': 3,
            },
            {
                'category': cat_event,
                'name': 'Event Management System',
                'slug': 'event-management-system',
                'product_type': 'core_product',
                'badge': 'Fast Gate Ticketing',
                'tagline': 'Instant QR gate check-in, attendee registration, ticket categories, and live entry reports.',
                'description': (
                    "Built for conference organizers, concert promoters, trade expos, and corporate summit hosts.\n\n"
                    "Clarity Event Management delivers lightning-fast QR code gate validation that works flawlessly offline at the entry gate, preventing long queues and ticket fraud."
                ),
                'architecture': 'High-Speed Gate Scanner & Ticket Management Platform',
                'features_list': (
                    "Sub-Second QR Gate Validation | Instant ticket verification scanning that works reliably even when mobile internet signals drop at busy venue gates.\n"
                    "Multi-Tier Ticket Categories | Configurable access levels, special door privileges, early access windows, and multi-day pass verification.\n"
                    "Live Gate Analytics Dashboard | Live attendance counter showing total entries, turnout percentage, hourly flow velocity, and peak arrival times.\n"
                    "On-Site Thermal Badge & Wristband Printing | Integrates with portable ESC/POS thermal printers and label machines to print name badges and receipts instantly."
                ),
                'minor_features': (
                    "Gate Operations: Rapid camera scanning on standard Android phones with no bulky hardware\n"
                    "Gate Operations: Support for rugged wireless 2D laser handheld scanners for high-volume gates\n"
                    "Gate Operations: Anti-passback security preventing duplicate scans of the same ticket\n"
                    "Gate Operations: Offline ticket verification database synced before doors open\n"
                    "Ticketing & Sales: Complimentary (comp) ticket allocation and VIP guest list management\n"
                    "Ticketing & Sales: Digital ticket delivery via WhatsApp, email PDF, and Apple Wallet pass\n"
                    "Ticketing & Sales: Box office cash sales module with thermal receipt printing at the door\n"
                    "Reporting & Post-Event: Complete attendee attendance roster export in Excel and CSV\n"
                    "Reporting & Post-Event: Gate-by-gate turnover and steward performance reports"
                ),
                'technical_specs': (
                    "Event Types: Conferences, Concerts, Trade Expos, Sports & Summits\n"
                    "Gate Speed: Rapid Under 1-Second QR Code Ticket Validation\n"
                    "Scanning Devices: Standard Android Phones or Handheld 2D Barcode Scanners\n"
                    "Ticket Formats: Digital PDF, WhatsApp Tickets & Printed Thermal Slips"
                ),
                'icon': 'fa-calendar-check',
                'logo_image': '',
                'mark_image': '',
                'accent_color': 'var(--color-maroon)',
                'price_amount': '25',
                'currency_symbol': '$',
                'billing_period': '/ event',
                'pricing_tagline': 'Sub-second QR gate scanning, ticket sales & live attendance analytics',
                'is_featured': True,
                'order': 4,
            },
        ]

        # Clean out any old Hub products if they exist
        hub_slugs = ['clarity-retail-hub', 'clarity-wholesale-hub', 'clarity-transporter-hub', 'clarity-exchange']
        Product.objects.filter(slug__in=hub_slugs).delete()

        products_map = {}
        for p_info in products_data:
            p_obj, _ = Product.objects.update_or_create(slug=p_info['slug'], defaults=p_info)
            products_map[p_info['slug']] = p_obj
        self.stdout.write("  [OK] Products seeded (4 Core Standalone Platforms)")

        # ── 5.1 Product Pricing Tiers ──────────────────────────────────────────
        tiers_data = [
            # Clarity Retail LAN Tiers (Starts at $30/m base)
            {
                'product': products_map['clarity-retail-lan'],
                'name': 'Single-Till Independent',
                'badge': 'Starter Counter',
                'tagline': 'Ideal for 1 independent branch operating a single checkout counter.',
                'price_amount': '30',
                'currency_symbol': '$',
                'billing_period': '/ store / mo',
                'branches_limit': '1 Retail Store',
                'tills_limit': '1 Till Workstation',
                'users_limit': 'Up to 3 Users',
                'features_list': (
                    "1 Store Location\n"
                    "1 Dedicated Counter Sales Till\n"
                    "Up to 3 Staff & Cashier Logins\n"
                    "100% Offline Autonomy Engine\n"
                    "Dual-Currency (USD & ZiG) Cash Register\n"
                    "Certified Fiscal Device Direct USB Driver\n"
                    "Daily Local Database Backup\n"
                    "Standard Business Hours Support"
                ),
                'is_featured': False,
                'cta_text': 'Book On-Site Consultation',
                'order': 1,
            },
            {
                'product': products_map['clarity-retail-lan'],
                'name': 'Multi-Till Retail Store',
                'badge': 'Most Popular',
                'tagline': 'Busy supermarket, spares shop, or retail counter with peer-to-peer LAN sync.',
                'price_amount': '59',
                'currency_symbol': '$',
                'billing_period': '/ store / mo',
                'branches_limit': '1 Retail Store',
                'tills_limit': 'Up to 4 Tills',
                'users_limit': 'Up to 10 Users',
                'features_list': (
                    "1 Store Location (Expandable)\n"
                    "Up to 4 Concurrent Tills on Local LAN\n"
                    "Up to 10 Staff & Cashier Accounts\n"
                    "Peer-to-Peer LAN Synchronization\n"
                    "Cashier Floating Floats & Blind Cash Drops\n"
                    "Supervisor Remote Void & Price Overrides\n"
                    "Priority WhatsApp Support SLA"
                ),
                'is_featured': True,
                'cta_text': 'Book On-Site Consultation',
                'order': 2,
            },
            {
                'product': products_map['clarity-retail-lan'],
                'name': 'Multi-Branch Retail Chain',
                'badge': 'Enterprise Scale',
                'tagline': 'Expanding retail chain with centralized master catalog and cross-branch sync.',
                'price_amount': '99',
                'currency_symbol': '$',
                'billing_period': '/ branch / mo',
                'branches_limit': 'Multi-Branch Network',
                'tills_limit': 'Scalable Tills (Per Store)',
                'users_limit': 'Unlimited User Accounts',
                'features_list': (
                    "Multi-Branch Retail Store Network\n"
                    "Unlimited Concurrent POS Tills per Branch\n"
                    "Centralized Catalog & Price Push\n"
                    "Cross-Branch Inventory Visibility\n"
                    "Automated Nightly Cloud Backup\n"
                    "Dedicated SLA & 24/7 Hotline"
                ),
                'is_featured': False,
                'cta_text': 'Book On-Site Consultation',
                'order': 3,
            },
            # Clarity Wholesale LAN Tiers
            {
                'product': products_map['clarity-wholesale-lan'],
                'name': 'Single Depot Wholesale',
                'badge': 'Depot Starter',
                'tagline': 'Single wholesale depot with up to 3 invoicing desks and 8 staff accounts.',
                'price_amount': '89',
                'currency_symbol': '$',
                'billing_period': '/ depot / mo',
                'branches_limit': '1 Wholesale Depot',
                'tills_limit': 'Up to 3 Invoicing Desks',
                'users_limit': 'Up to 8 Users',
                'features_list': (
                    "1 Depot Facility\n"
                    "Up to 3 Counter Invoicing Desks\n"
                    "Up to 8 Staff Accounts\n"
                    "Bulk Packaging Units & Auto-Conversion\n"
                    "Debtor Accounts & Credit Limit Warnings\n"
                    "Loading Bay Gate Pass Verification"
                ),
                'is_featured': False,
                'cta_text': 'Book On-Site Consultation',
                'order': 4,
            },
            {
                'product': products_map['clarity-wholesale-lan'],
                'name': 'High-Volume Wholesale Depot',
                'badge': 'Most Popular',
                'tagline': 'High-turnover multi-bay depot with automated GRV and customer credit limit controls.',
                'price_amount': '189',
                'currency_symbol': '$',
                'billing_period': '/ depot / mo',
                'branches_limit': 'Up to 2 Depots / Bays',
                'tills_limit': 'Up to 8 Invoicing Desks',
                'users_limit': 'Up to 20 Users',
                'features_list': (
                    "Up to 2 Depots / Dispatch Bays\n"
                    "Up to 8 Concurrent Invoicing Desks\n"
                    "Up to 20 Staff Logins\n"
                    "Automated Goods Received Vouchers (GRVs)\n"
                    "Mechanic Tiered Pricing Schedules\n"
                    "Picking Slip & Staging Verification"
                ),
                'is_featured': True,
                'cta_text': 'Book On-Site Consultation',
                'order': 5,
            },
            {
                'product': products_map['clarity-wholesale-lan'],
                'name': 'Multi-Depot Enterprise Network',
                'badge': 'National Fleet',
                'tagline': 'Nationwide wholesale distribution network with unlimited invoicing bays and ERP synchronization.',
                'price_amount': '299',
                'currency_symbol': '$',
                'billing_period': '/ enterprise / mo',
                'branches_limit': 'Multi-Depot Nationwide',
                'tills_limit': 'Unlimited Invoicing Bays',
                'users_limit': 'Unlimited Staff Accounts',
                'features_list': (
                    "Nationwide Wholesale Distribution Hubs\n"
                    "Unlimited Invoicing Bays & Users\n"
                    "Container Landed Cost Allocation\n"
                    "Enterprise ERP Integration (SAP, Sage, Pastel)\n"
                    "Priority Field Engineer Dispatch"
                ),
                'is_featured': False,
                'cta_text': 'Book On-Site Consultation',
                'order': 6,
            },
            # Hostel Management System Tiers
            {
                'product': products_map['hostel-management-system'],
                'name': 'Single Hostel Complex',
                'badge': 'Standard Hostel',
                'tagline': 'Independent student hostel and boarding house up to 150 beds.',
                'price_amount': '30',
                'currency_symbol': '$',
                'billing_period': '/ hostel / mo',
                'branches_limit': '1 Property Building',
                'tills_limit': 'Up to 2 Admin Stations',
                'users_limit': 'Up to 5 Staff Logins',
                'features_list': (
                    "Up to 150 Bed Accommodation Capacity\n"
                    "Visual Room & Bed Allocation Matrix\n"
                    "Student Rent & Security Deposit Ledger\n"
                    "Automated Rent Receipts via Email & Printout\n"
                    "Basic Maintenance Issue Logging"
                ),
                'is_featured': False,
                'cta_text': 'Book On-Site Consultation',
                'order': 7,
            },
            {
                'product': products_map['hostel-management-system'],
                'name': 'Multi-Property Campus Pro',
                'badge': 'Campus Scale',
                'tagline': 'Multi-building hostel complexes and university student accommodation.',
                'price_amount': '69',
                'currency_symbol': '$',
                'billing_period': '/ campus / mo',
                'branches_limit': 'Multi-Building Campus',
                'tills_limit': 'Unlimited Admin Desks',
                'users_limit': 'Unlimited Staff Accounts',
                'features_list': (
                    "Multi-Building Campus Portfolio\n"
                    "Unlimited Bed Sizing & Student Profiles\n"
                    "Parent & Student SMS Notification Integration\n"
                    "Comprehensive Overdue Rent Aging Reports\n"
                    "Priority Phone & On-Site Assistance"
                ),
                'is_featured': True,
                'cta_text': 'Book On-Site Consultation',
                'order': 8,
            },
            # Event Management System Tiers
            {
                'product': products_map['event-management-system'],
                'name': 'Single Event Pass',
                'badge': 'Single Event',
                'tagline': 'Single ticketed summit, concert, seminar, or banquet.',
                'price_amount': '25',
                'currency_symbol': '$',
                'billing_period': '/ event',
                'branches_limit': '1 Event Venue',
                'tills_limit': 'Up to 2 Gate Check-In Scanners',
                'users_limit': 'Up to 5 Event Staff Logins',
                'features_list': (
                    "1 Ticketed Event or Exhibition\n"
                    "Sub-Second Offline QR Code Ticket Scanner\n"
                    "Attendee Registration Roster & Check-In Status\n"
                    "Exportable Excel Turnout List"
                ),
                'is_featured': False,
                'cta_text': 'Book On-Site Consultation',
                'order': 9,
            },
            {
                'product': products_map['event-management-system'],
                'name': 'Annual Event Organizer',
                'badge': 'Organizer Choice',
                'tagline': 'Unlimited events, multi-gate scanners, and priority event-day SLA.',
                'price_amount': '59',
                'currency_symbol': '$',
                'billing_period': '/ organizer / mo',
                'branches_limit': 'Unlimited Event Venues',
                'tills_limit': 'Unlimited Gate Scanners',
                'users_limit': 'Unlimited Staff Accounts',
                'features_list': (
                    "Unlimited Events Throughout the Year\n"
                    "Multi-Gate Simultaneous QR Validation\n"
                    "Custom Attendee Badge & Wristband Printing\n"
                    "Live Attendance & Turnout Reports Dashboard\n"
                    "Event-Day Dedicated Technical Support"
                ),
                'is_featured': True,
                'cta_text': 'Book On-Site Consultation',
                'order': 10,
            },
        ]

        for t_info in tiers_data:
            ProductPricingTier.objects.update_or_create(
                product=t_info['product'],
                name=t_info['name'],
                defaults=t_info
            )
        self.stdout.write("  [OK] Product Pricing Tiers seeded (with $30/m base rate)")

        # ── 8. Hardware Products ───────────────────────────────────────────────
        hardware_data = [
            {
                'name': 'Thermal POS Receipt Printers',
                'slug': 'pos-printers',
                'hardware_category': 'POS Printers',
                'tagline': 'High-speed 80mm thermal receipt printing with auto-cutter and drawer kickout',
                'description': 'Heavy-duty 80mm thermal receipt printers engineered for continuous checkout environments. Featuring ultra-fast 260mm/s print speeds, a 1.5 million cut heavy-duty auto-cutter, and direct cash drawer kickout triggers.',
                'icon': 'fa-print',
                'price_min': '130',
                'price_max': '220',
                'price_unit': '/ unit',
                'warranty': '12-Month Free Swap-Out Warranty',
                'badge': 'Till Certified',
                'specs_list': 'Print Speed: 260 mm/s high-speed thermal\nPaper Width: 80mm (3 1/8 inch) standard receipt roll\nAuto-Cutter: Full or partial cut rated for 1.5M operations\nInterfaces: USB + Ethernet (LAN) + Serial RS-232\nCash Drawer Port: RJ11 / RJ12 24V pulse trigger\nCommand Compatibility: ESC/POS emulation standard',
                'key_features': 'Drop-in paper roll loading for rapid till turnover\nPaper-end and cover-open optical sensor alerts\nBuilt-in wall-mount or flat counter positioning\nFully tested and zero-driver compatible with Clarity POS',
                'order': 1
            },
            {
                'name': 'Commercial A4 Laser & Multi-Function Printers',
                'slug': 'a4-printers',
                'hardware_category': 'A4 Printers',
                'tagline': 'Heavy-duty duplex A4 printing for tax invoices, delivery notes, and dispatch manifests',
                'description': 'High-capacity A4 laser printers designed to handle high-volume wholesale depot operations, branch accounting statements, picking slips, and official transporter delivery manifests.',
                'icon': 'fa-file-lines',
                'price_min': '280',
                'price_max': '650',
                'price_unit': '/ unit',
                'warranty': '12-Month On-Site Manufacturer Warranty',
                'badge': 'Depot Workhorse',
                'specs_list': 'Print Speed: 38 - 45 pages per minute\nPaper Sizes: A4, Letter, Legal, Custom stationery\nDuplexing: Automatic two-sided printing standard\nDuty Cycle: Up to 80,000 pages per month\nConnectivity: Gigabit Ethernet, Wi-Fi 802.11ac, Hi-Speed USB 2.0\nPaper Input: 250-sheet internal cassette + 100-sheet multipurpose tray',
                'key_features': 'High-yield toner cartridges for lowest cost-per-page ratio\nInstant warm-up technology with first page out in < 6.5s\nNetwork print server enables shared printing across all depot tills\nSeamless invoice printing from Clarity Wholesale LAN & Hub',
                'order': 2
            },
            {
                'name': 'Industrial 1D & 2D Optical Barcode Readers',
                'slug': 'barcode-readers',
                'hardware_category': 'Barcode Readers',
                'tagline': 'Rapid omnidirectional scanning for scratched, faded, or phone-screen barcodes',
                'description': 'Rugged high-performance 1D/2D optical barcode scanners equipped with advanced CMOS imaging. Scans damaged, wrinkled, or low-contrast barcodes instantly, as well as electronic QR codes and vouchers off smartphone screens.',
                'icon': 'fa-barcode',
                'price_min': '45',
                'price_max': '120',
                'price_unit': '/ unit',
                'warranty': '12-Month Hardware Replacement Warranty',
                'badge': 'High Throughput',
                'specs_list': 'Scan Sensor: 1280 x 800 high-resolution CMOS imager\n1D Symbologies: UPC-A, EAN-13, Code 128, Code 39, ITF-14\n2D Symbologies: QR Code, DataMatrix, PDF417, Aztec\nScan Rate: 300 scans per second with sub-40ms decoding\nDrop Rating: Engineered to survive repeated 1.8m concrete drops\nInterface: USB HID Keyboard Wedge & Virtual COM plug-and-play',
                'key_features': 'Includes weighted ergonomic counter stand with auto-induction scanning\nAudible chime and clear top LED good-read confirmation\nScans directly from reflective smartphone screens for loyalty and coupons\nZero-configuration plug-and-play with Clarity Retail LAN tills',
                'order': 3
            },
            {
                'name': 'Enterprise Point-of-Sale & Management Laptops',
                'slug': 'laptops',
                'hardware_category': 'Laptops',
                'tagline': 'Rugged business-grade laptops for till terminals, supervisor desks, and stock audits',
                'description': 'Business-grade laptops selected and configured for the rigorous environments of retail tills, store manager desks, and mobile warehouse receiving. Equipped with high-capacity batteries that keep tills operational during grid load shedding.',
                'icon': 'fa-laptop',
                'price_min': '480',
                'price_max': '950',
                'price_unit': '/ unit',
                'warranty': '12-Month Enterprise Warranty',
                'badge': 'Load-Shedding Proof',
                'specs_list': 'Processor: Intel Core i5 / AMD Ryzen 5 High-Efficiency\nMemory: 8GB - 16GB High-Speed DDR4 / DDR5\nStorage: 256GB - 512GB NVMe M.2 Solid State Drive\nScreen: 14" or 15.6" Full HD (1920x1080) Anti-Glare Display\nBattery Life: 8 - 12 Hours continuous till run time on battery\nConnectivity: Gigabit RJ45 LAN, Wi-Fi 6, 3x USB 3.2, HDMI, Bluetooth',
                'key_features': 'Solid-state architecture provides sub-second transaction processing\nBuilt-in battery prevents till drops during sudden power cuts\nPre-loaded with Clarity Local Appliance OS and hardware drivers\nSpill-resistant keyboard and durable composite chassis',
                'order': 4
            },
            {
                'name': 'Network Equipment & Shielded Ethernet Cables',
                'slug': 'network-equipment-cables',
                'hardware_category': 'Network Infrastructure',
                'tagline': 'Enterprise gigabit switches, routers, and shielded Cat6 cabling for zero-jitter till LANs',
                'description': 'Certified network infrastructure hardware and high-grade shielded cabling designed to eliminate till drops, electromagnetic interference, and data packet loss between POS tills and the local Clarity server appliance.',
                'icon': 'fa-network-wired',
                'price_min': '85',
                'price_max': '480',
                'price_unit': '/ kit or spool',
                'warranty': '5-Year Structured Cabling Guarantee',
                'badge': 'Zero Packet Loss',
                'specs_list': 'Cabling: Cat6 / Cat6A 23AWG Solid Bare Copper UTP/FTP (305m pull-box)\nManaged Switches: 8-Port, 16-Port & 24-Port Gigabit with 802.3at PoE+\nRouters: Dual-WAN Enterprise Gigabit VPN Router with 4G/LTE failover\nPatch Panels: 24-Port Cat6 Rack-Mount with cable management bars\nConnectors: Gold-plated 50-micron RJ45 modular plugs with protective boots',
                'key_features': 'Pure copper conductors ensure maximum transmission speed without signal drop\nDual-WAN router automatically fails over to cellular backup if fiber disconnects\nPoE+ ports power security cameras and Wi-Fi access points without separate AC adapters\nStaged and tested by Avail Technologies network technicians',
                'order': 5
            }
        ]
        for h in hardware_data:
            HardwareProduct.objects.update_or_create(slug=h['slug'], defaults=h)
        self.stdout.write("  [OK] Hardware Products seeded")

        # ── 9. Platform User Manuals ───────────────────────────────────────────
        manuals_count = seed_manuals_data()
        self.stdout.write(f"  [OK] Platform User Manuals seeded ({manuals_count} chapters)")

        # ── 10. Company Metrics ────────────────────────────────────────────────
        metrics_data = [
            {'label': 'Store Sales Uptime', 'value': '100%', 'order': 1},
            {'label': 'Multi-Currency Checkout', 'value': 'Instant', 'order': 2},
            {'label': 'ZIMRA Fiscal Compliant', 'value': 'Certified', 'order': 3},
            {'label': 'Client Satisfaction Rate', 'value': '99.4%', 'order': 4},
        ]
        for m in metrics_data:
            CompanyMetric.objects.update_or_create(label=m['label'], defaults=m)
        self.stdout.write("  [OK] Company Metrics seeded")

        # ── 11. FAQ Items ──────────────────────────────────────────────────────
        faq_data = [
            {
                'category': 'Store Operations',
                'question': 'Does the counter checkout stop working if our store internet cuts out?',
                'answer': 'No, never. Clarity Retail operates 100% reliably on your in-store counter system. All barcode scanning, till receipts, and cash drawer drops continue without interruption even if your internet connection is completely offline. Once internet restores, all sales and shift records automatically synchronize to your central management dashboard.',
                'order': 1
            },
            {
                'category': 'Store Operations',
                'question': 'How does multi-store synchronization work across distributed retail branches?',
                'answer': 'Each store branch operates independently so sales never stop. Cashiers ring up sales locally, and your inventory updates in real time. Whenever internet or mobile connection is available, your branch automatically synchronizes all records to your head office dashboard, giving you instant visibility into branch sales, profits, and stock levels from any phone or PC.',
                'order': 2
            },
            {
                'category': 'Fiscal & Tax Compliance',
                'question': 'Is Clarity certified for ZIMRA fiscalisation and Electronic Signature Devices (ESD)?',
                'answer': 'Yes. Clarity connects directly to certified fiscal signature devices and fiscal printers, automatically signing receipts and printing statutory QR codes with zero cashier delays and 100% legal compliance.',
                'order': 3
            },
            {
                'category': 'Hardware & Equipment',
                'question': 'Can we use our existing barcode scanners, cash drawers, and thermal receipt printers?',
                'answer': 'Yes. Clarity is compatible with all standard thermal receipt printers (Epson, Bixolon, Xprinter, Rongta), standard cash drawers, and all standard USB and wireless 1D/2D barcode scanners right out of the box.',
                'order': 4
            },
            {
                'category': 'Hardware & Equipment',
                'question': 'What happens to our checkout tills during grid load shedding and power surges?',
                'answer': 'Our turnkey retail equipment bundles include energy-efficient counter mini-servers and till laptops with built-in battery backup, keeping your sales counters fully operational for 8 to 12 hours during power outages.',
                'order': 5
            },
            {
                'category': 'Support & Training',
                'question': 'What support and staff training is included after deployment?',
                'answer': 'We provide comprehensive hands-on cashier and manager training, dedicated WhatsApp telephone support, automatic daily cloud disaster recovery backups, and rapid on-site technician dispatch.',
                'order': 6
            },
        ]
        for f in faq_data:
            FAQItem.objects.update_or_create(question=f['question'], defaults=f)
        self.stdout.write("  [OK] FAQ Items seeded")

        # ── 12. Blog Categories & Posts ────────────────────────────────────────
        blog_cat, _ = BlogCategory.objects.get_or_create(
            slug='retail-operations',
            defaults={'name': 'Retail Operations & Growth', 'description': 'Practical guides and operational strategies for modern retail and wholesale businesses.'}
        )
        posts_data = [
            {
                'category': blog_cat,
                'title': 'Why African Retail Demands 100% Offline-Ready POS Systems',
                'slug': 'why-african-commerce-demands-offline-first',
                'excerpt': 'Why relying on cloud-only web POS systems causes lost revenue during telecom outages, and how in-store reliability protects your sales.',
                'content': (
                    "In retail and wholesale environments across Africa, internet connectivity and power grids can be unpredictable. "
                    "When a retail store uses a cloud-only POS, a severed fiber line or mobile network blackout immediately halts checkouts, "
                    "leading to long customer queues, abandoned baskets, and direct financial loss.\n\n"
                    "Clarity eliminates this vulnerability by keeping all sales logic, pricing, and fiscal receipt printing operational right inside the store. "
                    "Transactions take place instantly without waiting for cloud round-trips, ensuring your counters stay open and your customers stay happy."
                ),
                'author_name': 'Avail Technologies Retail Advisory',
                'author_role': 'Retail Systems Specialists',
                'read_time_minutes': 4,
                'is_featured': True,
                'is_published': True,
            },
            {
                'category': blog_cat,
                'title': 'The Auto Parts Retail Guide to Fast Part Lookups and Bin Locations',
                'slug': 'auto-parts-barcode-lookup-bin-locations',
                'excerpt': 'How structured OEM cross-referencing and shelf bin navigation speed up counter sales and eliminate customer return friction.',
                'content': (
                    "Managing auto parts inventory is fundamentally different from standard supermarket retail. "
                    "A single brake pad or water pump often matches a dozen different vehicle models across Toyota, Nissan, and Isuzu. "
                    "Counter salesmen must be able to search by OEM code, aftermarket part number, or vehicle model instantaneously.\n\n"
                    "Clarity Retail indexes over 50,000 part numbers directly in your store counter system, providing instant part lookups "
                    "and displaying exact shelf bin aisle coordinates so runners retrieve parts in seconds."
                ),
                'author_name': 'Avail Technologies Retail Advisory',
                'author_role': 'Retail Systems Specialists',
                'read_time_minutes': 5,
                'is_featured': True,
                'is_published': True,
            }
        ]
        for p in posts_data:
            Post.objects.update_or_create(slug=p['slug'], defaults=p)
        self.stdout.write("  [OK] Blog Articles seeded")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
