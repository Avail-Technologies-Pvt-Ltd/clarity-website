import os
import sys
import django

os.environ.update({
    'DJANGO_SETTINGS_MODULE': 'clarity_website.settings',
    'DB_NAME': 'dev_website',
    'DB_USER': 'dev_user',
    'DB_PASSWORD': 'dev_password',
    'DB_HOST': '127.0.0.1',
    'DB_PORT': '5439'
})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from products_showcase.models import ProductCategory, Product, ProductPricingTier

# 1. Categories
ProductCategory.objects.all().delete()

cat_retail = ProductCategory.objects.create(
    slug='motor-spares-retail',
    name='Motor Spares & Auto Retail',
    icon='fa-car',
    order=1
)

cat_wholesale = ProductCategory.objects.create(
    slug='motor-spares-wholesale',
    name='Motor Spares Wholesale & Importers',
    icon='fa-truck-ramp-box',
    order=2
)

cat_hostel = ProductCategory.objects.create(
    slug='hostel-management',
    name='Student Hostels & Accommodation',
    icon='fa-bed',
    order=3
)

cat_event = ProductCategory.objects.create(
    slug='event-management',
    name='Events & Conferences',
    icon='fa-calendar-check',
    order=4
)

# 2. Products We Sell as a Company

# A. Clarity Retail LAN (Motor Spares Retail Shop & Counter Sales)
p_retail = Product.objects.filter(slug='clarity-retail-lan').first()
if not p_retail:
    p_retail = Product(slug='clarity-retail-lan')
p_retail.category = cat_retail
p_retail.name = 'Clarity Retail LAN'
p_retail.product_type = 'core_product'
p_retail.badge = 'Motor Spares Counter POS'
p_retail.tagline = 'Fast auto parts counter sales, part number lookups, and stock tracking that never stops selling'
p_retail.description = (
    "Clarity Retail LAN is purpose-built for motor spares shops, auto parts retailers, and replacement parts counters. "
    "Your sales staff can search for parts instantly by part number, OEM reference, or car make and model "
    "(such as Toyota, Nissan, Isuzu, or Ford) to find the right part in seconds. "
    "Print instant counter quotes for customers and mechanics, check shelf and bin locations, and ring up sales with zero queue delays. "
    "Because the system runs inside your shop on a local computer, your counter keeps selling and printing receipts "
    "even when the internet cuts off or grid power flickers."
)
p_retail.architecture = 'Runs in Your Spares Shop (Offline Ready)'
p_retail.icon = 'fa-car'
p_retail.price_amount = '49'
p_retail.billing_period = '/ store / mo'
p_retail.pricing_tagline = 'Includes parts counter software, local shop server, part search, and backup database'
p_retail.features_list = """Part Number & Car Model Search | Search spare parts instantly by part number, OEM code, or vehicle make, model, and engine year.
Keep Selling When Internet Is Down | Counter sales and receipt printing keep running 100% locally with zero internet dependency.
Shelf & Bin Location Labels | See the exact aisle, shelf, and bin number on screen so counter runners fetch parts immediately.
Instant Counter Quotes & Invoices | Generate quick price quotes for walk-in customers and mechanics before they commit to buy.
Old Part / Core Returns & Warranties | Easily handle battery deposit returns, part warranties, and defective part exchanges."""
p_retail.technical_specs = """Built For: Retail motor spares shops, auto parts counters, automotive accessories
Search Engine: Part number, cross-reference brand, vehicle make/model/year
Storage Locations: Aisle, shelf, and bin location labels
Printers Supported: 80mm thermal receipt printers, counter laser printers
Cashier Controls: Shift float tracking, price override authorization, cash drawer kickout"""
p_retail.is_featured = True
p_retail.order = 1
p_retail.save()

# Pricing Tiers for Retail LAN
ProductPricingTier.objects.filter(product=p_retail).delete()
ProductPricingTier.objects.create(
    product=p_retail,
    name='Single Counter Spares Shop',
    tagline='For independent motor spares shops with 1-2 counter terminals',
    price_amount='49',
    price_annual='39',
    billing_period='/ store / mo',
    billing_period_annual='/ store / mo, billed annually',
    currency_symbol='$',
    features_list="Up to 2 counter terminals\nPart number & vehicle model search\nShelf & bin storage locations\nInstant counter quote printing\nDaily cashier cash-up reports\nLocal offline database engine",
    badge='Independent Shop',
    is_featured=False,
    order=1
)
ProductPricingTier.objects.create(
    product=p_retail,
    name='Busy Spares Counter Pro',
    tagline='For high-volume auto parts retailers with multiple sales counters',
    price_amount='89',
    price_annual='71',
    billing_period='/ store / mo',
    billing_period_annual='/ store / mo, billed annually',
    currency_symbol='$',
    features_list="Up to 6 counter terminals & runners\nUnlimited automotive parts catalog\nBattery & core exchange returns\nMechanic trade discount profiles\nShelf barcode printing & stock audits\nCloud backup & priority support",
    badge='Most Popular',
    is_featured=True,
    order=2
)

# B. Clarity Wholesale LAN (Motor Spares Wholesale & Importers Depot)
p_wholesale = Product.objects.filter(slug='clarity-wholesale-lan').first()
if not p_wholesale:
    p_wholesale = Product(slug='clarity-wholesale-lan')
p_wholesale.category = cat_wholesale
p_wholesale.name = 'Clarity Wholesale LAN'
p_wholesale.product_type = 'core_product'
p_wholesale.badge = 'Auto Parts Wholesale Depot'
p_wholesale.tagline = 'Bulk auto parts inventory, mechanic price lists, container receiving, and delivery dispatches'
p_wholesale.description = (
    "Clarity Wholesale LAN is designed specifically for motor spare parts importers, bulk automotive distributors, "
    "and fleet parts depots. Manage thousands of fast-moving and slow-moving parts, set up customized wholesale price lists "
    "for garages, fleet owners, and retail shops, and handle container shipments effortlessly from receiving bays to dispatch delivery vans."
)
p_wholesale.architecture = 'Runs in Your Parts Depot (Offline Ready)'
p_wholesale.icon = 'fa-truck-ramp-box'
p_wholesale.price_amount = '149'
p_wholesale.billing_period = '/ depot / mo'
p_wholesale.pricing_tagline = 'Includes trade sales desk, mechanic accounts, receiving bay, and multi-user access'
p_wholesale.features_list = """Tiered Trade & Mechanic Pricing | Set up distinct price lists for mechanics, transport fleets, reseller spares shops, and walk-in trade.
Bulk Container & Carton Breakdown | Receive bulk sea-freight shipments and break down wholesale cartons into shelf stock easily.
Trade Accounts & Credit Ledgers | Keep track of mechanic credit lines, unpaid balances, and generate monthly customer statements.
Warehouse Picking Slips & Delivery Notes | Print clear picking lists for warehouse staff and professional A4 delivery manifests for dispatch vans.
Fast-Moving vs Slow Stock Reports | Spot top-selling service parts (oil filters, brake pads) versus slow-moving engine rebuild kits."""
p_wholesale.technical_specs = """Built For: Auto parts importers, regional spares wholesalers, fleet maintenance depots
Pricing Engine: Tiered pricing by customer type (Garages, Fleets, Resellers, Retail)
Catalog Capacity: High-volume automotive part catalogs (OEM & aftermarket cross-references)
Invoicing: A4 trade tax invoices, delivery notes, and 80mm cash counter receipts
Dispatch Support: Delivery van loading manifests and dispatch bay tracking"""
p_wholesale.is_featured = True
p_wholesale.order = 2
p_wholesale.save()

# Pricing Tiers for Wholesale LAN
ProductPricingTier.objects.filter(product=p_wholesale).delete()
ProductPricingTier.objects.create(
    product=p_wholesale,
    name='Wholesale Spares Depot',
    tagline='For regional auto parts distributors and single wholesale depots',
    price_amount='149',
    price_annual='119',
    billing_period='/ depot / mo',
    billing_period_annual='/ depot / mo, billed annually',
    currency_symbol='$',
    features_list="Up to 5 trade desk & receiving stations\nTiered pricing (Garages, Fleet, Resellers)\nTrade customer credit limits & ledgers\nA4 delivery notes & picking lists\nContainer shipment receiving breakdown\nDedicated local depot server",
    badge='Depot Standard',
    is_featured=False,
    order=1
)
ProductPricingTier.objects.create(
    product=p_wholesale,
    name='Enterprise Parts Importer',
    tagline='For high-volume automotive importers and master supply depots',
    price_amount='249',
    price_annual='199',
    billing_period='/ depot / mo',
    billing_period_annual='/ depot / mo, billed annually',
    currency_symbol='$',
    features_list="Unlimited trade desks & warehouse terminals\nCross-reference OEM & aftermarket database\nDelivery van dispatch & waybill logs\nSlow-moving & dead stock analytics\nMulti-currency trade invoicing\nDedicated account engineer",
    badge='Importers Choice',
    is_featured=True,
    order=2
)

# C. Hostel Management System
p_hostel = Product.objects.filter(slug='hostel-management-system').first()
if not p_hostel:
    p_hostel = Product(slug='hostel-management-system')
p_hostel.category = cat_hostel
p_hostel.name = 'Hostel Management System'
p_hostel.product_type = 'core_product'
p_hostel.badge = 'Student Accommodation'
p_hostel.tagline = 'Effortless room allocations, student bookings, fee collection, and resident management'
p_hostel.description = (
    "A clean, simple software system designed for student hostels, university boarding houses, and private student accommodation. "
    "Easily see room availability, assign beds, collect student rent payments, track security gate check-ins, "
    "and manage maintenance requests from one easy dashboard."
)
p_hostel.architecture = 'Cloud & Local Multi-User'
p_hostel.icon = 'fa-bed'
p_hostel.price_amount = '39'
p_hostel.billing_period = '/ month'
p_hostel.pricing_tagline = 'Scales from single student buildings to multi-campus hostel complexes'
p_hostel.features_list = """Visual Room & Bed Allocations | See occupied, booked, and empty beds at a glance and allocate students in seconds.
Student Invoicing & Rent Tracking | Track rent payments, installments, caution fees, and outstanding student balances with automatic receipts.
Digital Student Directory | Store student identification photos, guardian emergency contacts, room keys, and signed agreements.
Maintenance & Damage Logging | Log room repair issues, track broken fixtures, and monitor room inspections before check-out.
Security Gate Access & Visitors | Record student curfew check-ins and log outside visitors for resident safety."""
p_hostel.technical_specs = """Supported Properties: Private student hostels, boarding houses, dormitories
Access: Runs securely in web browsers on laptops, tablets, and office PCs
Reports: Room occupancy percentage, fee collection summaries, unpaid balance statements
Printing: Student registration forms, rent payment receipts, check-in slips"""
p_hostel.is_featured = True
p_hostel.order = 3
p_hostel.save()

# D. Event Management System
p_event = Product.objects.filter(slug='event-management-system').first()
if not p_event:
    p_event = Product(slug='event-management-system')
p_event.category = cat_event
p_event.name = 'Event Management System'
p_event.product_type = 'core_product'
p_event.badge = 'Events & Ticketing'
p_event.tagline = 'Sell tickets, register attendees, print guest badges, and check people in smoothly'
p_event.description = (
    "Built for conference organizers, event planners, churches, and exhibition venues. "
    "Set up ticket types, send digital QR invitations, scan guest tickets at the door in under a second "
    "using your phone or barcode scanner, and manage venue bookings with zero double-booking."
)
p_event.architecture = 'Cloud & Fast Door Scanner'
p_event.icon = 'fa-calendar-check'
p_event.price_amount = '29'
p_event.billing_period = '/ event or mo'
p_event.pricing_tagline = 'Ideal for ticketed summits, concerts, corporate galas, and conferences'
p_event.features_list = """Sub-Second Door Check-In | Scan guest tickets off phone screens or printed paper in less than a second to eliminate door lines.
Custom Ticket Types & VIP Passes | Create Regular, VIP, and Group tickets with automatic digital ticket delivery.
Instant Badge & Name Tag Printing | Connect directly to label printers at your check-in counter to print attendee badges on the spot.
Real-Time Attendance Counts | Know exactly how many guests have arrived, who has checked in, and who has not yet arrived.
Venue & Hall Calendar Booking | Manage hall setup schedules, seating charts, and equipment bookings without double-booking."""
p_event.technical_specs = """Scanner Support: Works with handheld 2D optical barcode scanners, USB scanners, or smartphones
Ticket Delivery: Automatic email tickets with unique verification QR codes
Badge Formats: Standard guest name tags, thermal badges, and lanyard inserts
Export Options: Export attendee lists and financial sales reports to Excel or PDF"""
p_event.is_featured = True
p_event.order = 4
p_event.save()

# E. Cloud features specifically linked to LAN products (not sold standalone)
hub_retail = Product.objects.filter(slug='clarity-retail-hub').first()
if hub_retail:
    hub_retail.name = 'Clarity Retail Hub'
    hub_retail.product_type = 'cloud_feature'
    hub_retail.is_featured = False
    hub_retail.tagline = 'Cloud multi-branch dashboard for motor spares shop owners'
    hub_retail.access_description = 'Optional cloud add-on accessed via Clarity Retail LAN to view shop sales and update parts prices from anywhere.'
    hub_retail.save()

hub_wholesale = Product.objects.filter(slug='clarity-wholesale-hub').first()
if hub_wholesale:
    hub_wholesale.name = 'Clarity Wholesale Hub'
    hub_wholesale.product_type = 'cloud_feature'
    hub_wholesale.is_featured = False
    hub_wholesale.tagline = 'Multi-depot stock orchestrator for auto parts distributors'
    hub_wholesale.access_description = 'Optional cloud add-on accessed via Clarity Wholesale LAN to balance stock across multiple spares warehouses.'
    hub_wholesale.save()

hub_transporter = Product.objects.filter(slug='clarity-transporter-hub').first()
if hub_transporter:
    hub_transporter.name = 'Clarity Transporter Hub'
    hub_transporter.product_type = 'cloud_feature'
    hub_transporter.is_featured = False
    hub_transporter.tagline = 'Delivery van dispatch and parts waybills'
    hub_transporter.access_description = 'Optional cloud add-on accessed via Clarity Wholesale LAN to track parts delivery vans and mechanic drops.'
    hub_transporter.save()

exchange = Product.objects.filter(slug='clarity-exchange').first()
if exchange:
    exchange.name = 'Clarity Exchange'
    exchange.product_type = 'cloud_feature'
    exchange.is_featured = False
    exchange.tagline = 'Electronic B2B restock link between spares retailers and wholesale importers'
    exchange.access_description = 'Optional cloud add-on accessed via Wholesale LAN to receive orders electronically from retail spares shops.'
    exchange.save()

print('Software products successfully updated for Motor Spares, Hostels, and Events!')
