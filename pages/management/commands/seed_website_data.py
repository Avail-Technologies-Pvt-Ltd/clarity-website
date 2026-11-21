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
                'hero_eyebrow': 'Enterprise Systems & Software Engineering',
                'hero_headline': 'Architecting Exceptional Software Systems for African Commerce',
                'hero_subheadline': 'Bespoke digital solutions that redefine operational efficiency in motor spares, retail, and modern African enterprises. Local-first resilience with seamless cloud telemetry.',
                'vision_statement': "To be Africa's most trusted digital transformation partner, where every solution we deliver sets a new standard for operational excellence and business agility.",
                'mission_statement': 'To empower African businesses with intelligent, adaptive software that eliminates inefficiencies, accelerates decision-making, and unlocks unprecedented value, delivered with uncompromising quality and client-first dedication.',
                'about_story': 'Founded in 2023, Avail Technologies Pvt Ltd is a progressive software innovator, crafting bespoke digital solutions that redefine efficiency in African enterprises. We do not just build software, we pride ourselves in engineering growth.',
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
                'title': 'Autonomous Offline-First Edge Architectures',
                'slug': 'edge-systems',
                'short_summary': 'We engineer systems that execute high-concurrency transactions locally at the counter and warehouse floor with zero dependency on the internet or external cloud connections.',
                'full_description': (
                    "Power outages, severed fiber cables, and telecom carrier downtime cannot bring a commercial business to a halt. We architect distributed store and warehouse nodes where each terminal or cluster maintains its own ACID-compliant local database engine.\n\n"
                    "Cashiers ring sales, warehouse pickers scan cartons, and fiscal slips print in sub-40 milliseconds without touching the internet. When network uplinks restore, our conflict-free async replication queues stream delta transactions to headquarters automatically."
                ),
                'icon': 'fa-server',
                'technical_bullets': (
                    "Sub-40ms barcode scan and counter response\n"
                    "Zero downtime during fiber/LTE telecom outages\n"
                    "Async bidirectional synchronization with master catalog\n"
                    "Local transaction ledger with cryptographic hashing"
                ),
                'key_stat_number': '100%',
                'key_stat_label': 'Autonomous Uptime',
                'bento_span': 8,
                'order': 1,
            },
            {
                'pillar_number': 'Pillar 02',
                'title': 'Fiscal Device & Regulatory Engineering',
                'slug': 'fiscal-engineering',
                'short_summary': 'Direct low-level USB, Serial, and TCP interfaces to certified electronic tax registers, fiscal signature devices, and governmental revenue authorities.',
                'full_description': (
                    "Tax authorities across Africa enforce strict electronic fiscalisation laws requiring cryptographically signed receipts and instant QR verification. We build low-level hardware drivers and cloud fiscalisation middleware directly into our software engines.\n\n"
                    "Our systems interface seamlessly with Electronic Signature Devices (ESD), fiscal memory units, and direct tax authority REST endpoints, ensuring our clients maintain 100% legal compliance with zero checkout slowdowns."
                ),
                'icon': 'fa-receipt',
                'technical_bullets': (
                    "Certified Fiscal Printers & Signature Devices\n"
                    "High-Speed Auto Parts Barcode & 2D QR Readers\n"
                    "ESC/POS High-Speed Thermal Receipt Printers\n"
                    "Industrial Mobile Handheld Barcode Scanners"
                ),
                'key_stat_number': '100%',
                'key_stat_label': 'Statutory Fiscal Compliance',
                'bento_span': 4,
                'order': 2,
            },
            {
                'pillar_number': 'Pillar 03',
                'title': 'Turnkey Hardware Staging & Appliances',
                'slug': 'hardware-staging',
                'short_summary': 'Pre-configured, burn-in tested industrial mini-servers, touch till terminals, thermal printers, and fiscal devices delivered ready for immediate deployment.',
                'full_description': (
                    "Deploying retail and warehouse systems shouldn't require weeks of on-site IT troubleshooting. We supply pre-assembled, fully provisioned hardware kits.\n\n"
                    "Every store server appliance undergoes 72 hours of burn-in testing, SSD mirroring, and local database initialization before delivery to your branch location."
                ),
                'icon': 'fa-microchip',
                'technical_bullets': (
                    "Plug-and-play mini-servers with pre-installed Linux runtime\n"
                    "72-hour continuous thermal & electrical burn-in testing\n"
                    "Heavy-duty cash drawers & 80mm thermal receipt printers\n"
                    "On-site cabling, LAN stress testing & staff orientation"
                ),
                'key_stat_number': '< 2 Hrs',
                'key_stat_label': 'Average Branch Deployment Time',
                'bento_span': 4,
                'order': 3,
            },
            {
                'pillar_number': 'Pillar 04',
                'title': '24/7 Managed Operations & Emergency SLA',
                'slug': 'managed-operations',
                'short_summary': 'Around-the-clock telemetry monitoring, proactive data synchronization audits, automated cloud disaster recovery, and dedicated emergency field engineers.',
                'full_description': (
                    "Supermarkets, parts counters, and wholesale distribution depots cannot afford downtime during peak hours or weekend rushes. Our support agreements provide around-the-clock monitoring and emergency engineering response.\n\n"
                    "We monitor branch server heartbeats, disk health, and replication queues 24 hours a day to prevent outages before they happen."
                ),
                'icon': 'fa-shield-halved',
                'technical_bullets': (
                    "Sub-15 minute critical incident response time\n"
                    "Real-time heartbeat telemetry on store servers\n"
                    "Automated daily encrypted off-site cloud backups\n"
                    "Dedicated emergency field engineers & WhatsApp hotline"
                ),
                'key_stat_number': '99.9%',
                'key_stat_label': 'System Operational Availability',
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
                'title': 'Custom Retail & Warehouse Software Engineering',
                'slug': 'custom-engineering',
                'category_code': '01 / CORE ENGINEERING',
                'short_description': 'Bespoke point-of-sale workflows, multi-currency accounting logic, warehouse picking flows, and legacy database migration.',
                'full_description': 'Every retail chain has unique operational requirements that off-the-shelf software cannot satisfy. We engineer tailored software architectures.',
                'icon': 'fa-laptop-code',
                'deliverables_list': (
                    "Custom Point-of-Sale Checkout Workflows\n"
                    "Multi-Currency Cash Drawer Reconciliation (USD & ZiG)\n"
                    "Warehouse Bin-Location Picking & Packing\n"
                    "Legacy System Data Migration (Pastel, QuickBooks, Excel)"
                ),
                'turnkey_benefit': 'Software built around your exact commercial operational processes rather than forcing your business to adapt.',
                'price_amount': 'Custom',
                'currency_symbol': '',
                'billing_period': 'milestone-based',
                'pricing_model': 'Fixed-Scope Engineering SOW',
                'commercial_terms': (
                    "Comprehensive on-site operational discovery phase\n"
                    "Source-code escrow and IP protection\n"
                    "User Acceptance Testing (UAT) sign-off gates\n"
                    "Post-launch warranty & handover documentation"
                ),
                'order': 1,
                'is_featured': True,
            },
            {
                'title': 'Turnkey Hardware Staging & Deployment Kits',
                'slug': 'hardware-staging-service',
                'category_code': '02 / HARDWARE PROVISIONING',
                'short_description': 'Pre-assembled, burn-in tested industrial mini-servers, touch till terminals, thermal printers, and fiscal devices ready for immediate branch deployment.',
                'full_description': 'Deploying retail systems shouldn’t require weeks of IT troubleshooting. We supply complete turnkey hardware appliances.',
                'icon': 'fa-microchip',
                'deliverables_list': (
                    "Plug-and-Play Store Mini-Servers with Docker Edge Runtime\n"
                    "Thermal Receipt Printers & Heavy-Duty Cash Drawers\n"
                    "Industrial Barcode Label Printers & Optical Scanners\n"
                    "On-Site Cabling & Local LAN Stress Testing"
                ),
                'turnkey_benefit': 'Plug into the wall, connect the till monitors, and start ringing sales in under two hours.',
                'price_amount': '450',
                'currency_symbol': '$',
                'billing_period': 'one-off appliance kit',
                'pricing_model': 'Turnkey Appliance Staging',
                'commercial_terms': (
                    "Pre-installed Linux & Docker container edge runtime\n"
                    "72-hour continuous thermal & electrical burn-in testing\n"
                    "Dual SSD mirroring with battery backup power\n"
                    "3-Year hardware replacement warranty"
                ),
                'order': 2,
                'is_featured': True,
            },
            {
                'title': 'Fiscal Device & Compliance Integration',
                'slug': 'fiscal-integration',
                'category_code': '03 / FISCAL ENGINEERING',
                'short_description': 'Direct integration with certified Electronic Signature Devices (ESD), fiscal printers, and automated tax authority API synchronization.',
                'full_description': 'Navigating governmental tax compliance regulations can stall retail rollouts. We provide certified fiscal device integration, driver configuration, and tax authority API synchronization.',
                'icon': 'fa-file-invoice-dollar',
                'deliverables_list': (
                    "Certified Electronic Signature Device (ESD) Integration\n"
                    "Automated QR Code Signing & Daily Z-Reports\n"
                    "Real-Time Cloud Tax Authority Dispatch\n"
                    "Statutory Fiscal Memory Auditing"
                ),
                'turnkey_benefit': '100% compliant with local statutory revenue authority requirements with zero checkout slowdowns.',
                'price_amount': '250',
                'currency_symbol': '$',
                'billing_period': 'per device model',
                'pricing_model': 'Certified Driver & Fiscal Authority Integration',
                'commercial_terms': (
                    "Cryptographic Electronic Signature Device (ESD) firmware interface\n"
                    "Official governmental revenue authority test sign-off\n"
                    "Offline QR code generation with sub-20ms signing speed\n"
                    "Automated statutory daily Z-report generation"
                ),
                'order': 3,
                'is_featured': True,
            },
            {
                'title': '24/7 Managed Operations & Emergency SLA',
                'slug': 'managed-operations-service',
                'category_code': '04 / MANAGED INFRASTRUCTURE',
                'short_description': 'Around-the-clock telemetry monitoring, proactive data synchronization audits, automated cloud disaster recovery, and dedicated emergency field engineers.',
                'full_description': 'Supermarkets and distribution hubs cannot afford downtime during peak shopping hours or weekend rushes. Our support agreements provide around-the-clock monitoring and emergency engineering response.',
                'icon': 'fa-shield-halved',
                'deliverables_list': (
                    "Sub-15 Minute Critical Incident Response Time\n"
                    "Real-Time Heartbeat Telemetry on Store Servers\n"
                    "Automated Daily Off-Site Cloud Backups\n"
                    "Dedicated Emergency Field Engineers"
                ),
                'turnkey_benefit': 'Standard, Priority, and Mission-Critical SLAs with downtime penalty guarantees.',
                'price_amount': '150',
                'currency_symbol': '$',
                'billing_period': '/ store / mo',
                'pricing_model': 'Proactive SLA & Managed Operations',
                'commercial_terms': (
                    "24/7/365 telemetry monitoring with sub-15 min critical response\n"
                    "Automated daily encrypted off-site cloud backups\n"
                    "Monthly database performance optimization & health check\n"
                    "Dedicated WhatsApp hotline & field engineer dispatch"
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
                    "100% Offline Autonomous Local Database Engine\n"
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
                    "Priority Engineering & SLA"
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
                    "24/7 Emergency SLA & Dedicated Solutions Architect"
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
                'tagline': 'Industrial mini-server with battery power and pre-installed PostgreSQL runtime.',
                'price_amount': '450',
                'currency_symbol': '$',
                'billing_period': 'one-off appliance',
                'features_list': (
                    "Pre-installed Linux & Docker Runtime\n"
                    "Handles up to 30 concurrent Till Lanes\n"
                    "Dual SSD Mirroring with Battery Backup\n"
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
                'badge': 'Offline-First POS',
                'tagline': 'Autonomous high-speed touch POS and in-store server appliance with zero internet dependency.',
                'description': (
                    "Clarity Retail LAN is the flagship store-level point-of-sale engine. Engineered to operate directly on the branch local area network, it eliminates checkout downtime during internet or telecommunication blackouts.\n\n"
                    "With sub-40ms barcode scan response, cashier floating drawers, integrated weight scales, and certified fiscal device drivers, Retail LAN delivers continuous retail execution without cloud interruptions."
                ),
                'architecture': 'Local PostgreSQL / SQLite Store Engine + Async Queue',
                'features_list': (
                    "100% Offline Autonomy | Ring sales, apply promotional discounts, and issue tax receipts without internet.\n"
                    "Multi-Till Synchronization | Instant shared till numbers, price lookups, and inventory reservations across all lanes.\n"
                    "Fiscal Device Certified | Native USB and Serial drivers for electronic signature devices and fiscal printers.\n"
                    "Dual Currency Cash Register | Simultaneous handling of USD, local currencies, split payments, and end-of-shift denomination counting.\n"
                    "Blind Cash Drops & Audit Shield | Supervisor overrides for line voids, refunds, and real-time drawer opening alerts."
                ),
                'technical_specs': (
                    "Deployment Mode: On-Premise Store Server Appliance (Bare-metal or Docker)\n"
                    "Database Engine: PostgreSQL 13+ / SQLite Embedded\n"
                    "Till Interface: Modern Web Touchscreen / Android POS\n"
                    "Peripherals: ESC/POS Thermal, Fiscal Devices, Barcode Scales, Cash Drawers\n"
                    "Checkout Latency: < 40ms Barcode Lookup"
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
                'badge': 'Wholesale Depot LAN',
                'tagline': 'High-volume auto parts bulk inventory, mechanic price lists, container receiving, and delivery dispatches.',
                'description': (
                    "Built specifically for motor spares wholesale depots, automotive parts importers, and fleet distribution centers.\n\n"
                    "Clarity Wholesale LAN supports mechanic price lists, container receiving, carton breakdowns, debtor credit limits, and loading bay gate passes."
                ),
                'architecture': 'Local Warehouse Network Server + Dispatch Gateway',
                'features_list': (
                    "Multi-Tier Packaging Units | Sell goods by piece, pack, case, shrink-wrap, or pallet with auto-conversion.\n"
                    "Customer Credit Management | Track aging balances, payment terms, credit stops, and statement generation.\n"
                    "Loading Bay Staging | Separate invoice generation from warehouse picking and loading verification.\n"
                    "Gate Pass Security | Scannable dispatch passes verified by security personnel before trucks depart."
                ),
                'technical_specs': (
                    "Packaging Hierarchy: Unlimited Unit Nesting (Piece -> Pack -> Case -> Pallet)\n"
                    "Credit Ledger: Real-Time Debtor Aging & Credit Limit Locks\n"
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
                'badge': 'Accommodation Engine',
                'tagline': 'Modern student hostel, dorm, and boarding house management with room allocations and rent ledger.',
                'description': (
                    "An intuitive and reliable management platform designed specifically for private student hostels, university dorms, and residential complexes.\n\n"
                    "Manage room assignments, student leases, installment payment plans, maintenance tickets, and check-in rosters effortlessly."
                ),
                'architecture': 'Web Platform + Resident Portal + SMS Gateway',
                'features_list': (
                    "Visual Room & Bed Allocation | Interactive floor layout with occupancy status per room.\n"
                    "Student Rent & Deposit Ledger | Automatic payment receipts, balance tracking, and overdue reminders.\n"
                    "Maintenance Ticket Tracker | Track plumbing, electrical, and room repair requests from submission to resolution.\n"
                    "Gate Access & Resident Directory | Searchable student rosters with emergency contact details."
                ),
                'technical_specs': (
                    "Deployment Mode: Cloud Hosted or Local Campus Server\n"
                    "Capacity: Scales from 20 to 2,000+ bed student facilities\n"
                    "Access: Role-based permissions for warden, accountant, and administration"
                ),
                'icon': 'fa-bed',
                'logo_image': 'images/clarity-hostel-logo.png',
                'mark_image': 'images/clarity-hostel-mark.png',
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
                'badge': 'Ticketing & Gate Pass',
                'tagline': 'Fast QR gate ticketing, attendee registration, badge printing, and live admission analytics.',
                'description': (
                    "Built for conference organizers, concert promoters, trade expos, and corporate summit hosts.\n\n"
                    "Clarity Event Management delivers lightning-fast QR code gate validation that works flawlessly offline at the entry gate, preventing long queues and ticket fraud."
                ),
                'architecture': 'Offline-Capable Gate Scanner + Central Attendee Database',
                'features_list': (
                    "Sub-Second QR Gate Scanning | Instant ticket barcode verification that operates even during mobile signal dropouts.\n"
                    "Multi-Tier Ticket Categories | VIP, Early Bird, General Admission, and Exhibitor pass tiers with custom access privileges.\n"
                    "Real-Time Gate Analytics | Live dashboard showing attendance turnout velocity and entry gate traffic.\n"
                    "On-Site Badge & Wristband Printing | ESC/POS and direct thermal slip printer compatibility at check-in desks."
                ),
                'technical_specs': (
                    "Scan Speed: < 200ms per QR Ticket Validation\n"
                    "Scanning Hardware: Android Smartphone Camera, Honeywell USB, or Zebra 2D Scanners\n"
                    "Ticket Formats: Digital PDF, Apple Wallet, and Printed Thermal QR Slips"
                ),
                'icon': 'fa-calendar-check',
                'logo_image': 'images/clarity-event-logo.png',
                'mark_image': 'images/clarity-event-mark.png',
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
                    "Live Entry Velocity & Turnout Telemetry Dashboard\n"
                    "Event-Day On-Call Technical SLA"
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
            {'label': 'Edge Scan Latency', 'value': '< 40ms', 'order': 1},
            {'label': 'Offline Autonomy', 'value': '100%', 'order': 2},
            {'label': 'Telecom Outage Checkout Halts', 'value': '0%', 'order': 3},
            {'label': 'Client Retention Rate', 'value': '99.4%', 'order': 4},
        ]
        for m in metrics_data:
            CompanyMetric.objects.update_or_create(label=m['label'], defaults=m)
        self.stdout.write("  [OK] Company Metrics seeded")

        # ── 11. FAQ Items ──────────────────────────────────────────────────────
        faq_data = [
            {
                'category': 'Offline Architecture',
                'question': 'Does the counter checkout stop working if our store internet cuts out?',
                'answer': 'No, never. Clarity Retail LAN operates 100% autonomously on your local counter server appliance. All barcode scanning, till receipts, and cash drawer drops continue at sub-40 millisecond response speeds with zero dependency on internet connection. Once your internet restores, changes synchronize to headquarters in the background.',
                'order': 1
            },
            {
                'category': 'Offline Architecture',
                'question': 'How does multi-store synchronization work across distributed retail branches?',
                'answer': 'Each store maintains its own independent ACID-compliant local database. As sales occur, delta change events are queued cryptographically. When connectivity is available, transactions replicate upstream to your centralized Clarity Hub without blocking till operations.',
                'order': 2
            },
            {
                'category': 'Fiscal & Statutory',
                'question': 'Is Clarity certified for ZIMRA fiscalisation and Electronic Signature Devices (ESD)?',
                'answer': 'Yes. Clarity Retail integrates directly via USB, Serial, and Network protocols with certified fiscal signature devices and fiscal memory units, cryptographically signing receipts and printing statutory QR codes with zero cashier delays.',
                'order': 3
            },
            {
                'category': 'Hardware & Staging',
                'question': 'Can we use our existing barcode scanners, cash drawers, and thermal receipt printers?',
                'answer': 'Yes. Clarity supports standard ESC/POS thermal receipt printers (Epson, Bixolon, Xprinter, Rongta), standard 24V RJ11/RJ12 cash drawers, and all standard USB and wireless 1D/2D barcode scanners out of the box without proprietary drivers.',
                'order': 4
            },
            {
                'category': 'Hardware & Staging',
                'question': 'What happens to the POS during grid load shedding and power surges?',
                'answer': 'Our turnkey retail hardware bundles feature energy-efficient mini-servers and till laptops with built-in battery backup, keeping your counter fully operational for 8 to 12 hours during severe power grid outages.',
                'order': 5
            },
            {
                'category': 'Support & SLA',
                'question': 'What support is included after deployment?',
                'answer': 'We offer dedicated SLA support packages including 24/7 emergency telephone hotlines, sub-15 minute critical incident response times, daily encrypted cloud disaster recovery backups, and on-site emergency field technicians.',
                'order': 6
            },
        ]
        for f in faq_data:
            FAQItem.objects.update_or_create(question=f['question'], defaults=f)
        self.stdout.write("  [OK] FAQ Items seeded")

        # ── 12. Blog Categories & Posts ────────────────────────────────────────
        blog_cat, _ = BlogCategory.objects.get_or_create(
            slug='engineering-architecture',
            defaults={'name': 'Engineering & Architecture', 'description': 'Deep dives into resilient, offline-first systems design.'}
        )
        posts_data = [
            {
                'category': blog_cat,
                'title': 'Why African Commerce Demands Autonomous Offline-First Architecture',
                'slug': 'why-african-commerce-demands-offline-first',
                'excerpt': 'Why relying on cloud-only web point-of-sale systems causes catastrophic revenue loss during telecom carrier outages, and how distributed edge computing solves it.',
                'content': (
                    "In modern retail and wholesale environments across Africa, internet connectivity and power grids are unpredictable. "
                    "When a retail store uses a cloud-only POS, a severed fiber line or LTE carrier blackout immediately paralyzes checkouts, "
                    "causing abandoned carts, long queues, and direct revenue loss.\n\n"
                    "Clarity was architected from day one to eliminate cloud single points of failure. By executing all business logic, "
                    "pricing calculations, and fiscal receipt signing on the local store server appliance, transactions complete in under 40 milliseconds "
                    "regardless of whether the outside world is online or completely disconnected."
                ),
                'author_name': 'Avail Technologies Engineering Squad',
                'author_role': 'Core Systems Architects',
                'read_time_minutes': 4,
                'is_featured': True,
                'is_published': True,
            },
            {
                'category': blog_cat,
                'title': 'The Auto Parts Retail Guide to Sub-40ms Barcode Lookups and Bin Locations',
                'slug': 'auto-parts-barcode-lookup-bin-locations',
                'excerpt': 'How structured OEM cross-referencing and shelf bin navigation accelerate counter turnover and eliminate customer return friction.',
                'content': (
                    "Managing auto parts inventory is fundamentally different from standard supermarket retail. "
                    "A single brake pad or water pump often matches a dozen different vehicle applications across Toyota, Nissan, and Isuzu. "
                    "Counter salesmen must be able to query by OEM code, aftermarket part number, or vehicle model code instantaneously.\n\n"
                    "Clarity Retail LAN indexes over 50,000 part numbers directly on the local machine, providing instant sub-second lookup "
                    "and displaying exact shelf bin aisle coordinates so runners retrieve parts in seconds."
                ),
                'author_name': 'Avail Technologies Engineering Squad',
                'author_role': 'Retail Solutions Architect',
                'read_time_minutes': 5,
                'is_featured': True,
                'is_published': True,
            }
        ]
        for p in posts_data:
            Post.objects.update_or_create(slug=p['slug'], defaults=p)
        self.stdout.write("  [OK] Blog Articles seeded")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
