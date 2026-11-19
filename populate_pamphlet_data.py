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

from pages.models import CompanyProfile, Service
from products_showcase.models import HardwareProduct

# 1. Update CompanyProfile
cp, _ = CompanyProfile.objects.get_or_create(id=1)
cp.company_name = 'Avail Technologies (Pvt) Ltd'
cp.hero_eyebrow = 'Enterprise Systems & Software Engineering'
cp.hero_headline = 'Architecting Exceptional Software Systems for African Commerce'
cp.hero_subheadline = 'Bespoke digital solutions that redefine operational efficiency in motor spares, retail, and modern African enterprises. Local-first resilience with seamless cloud telemetry.'
cp.vision_statement = "To be Africa's most trusted digital transformation partner, where every solution we deliver sets a new standard for operational excellence and business agility."
cp.mission_statement = 'To empower African businesses with intelligent, adaptive software that eliminates inefficiencies, accelerates decision-making, and unlocks unprecedented value, delivered with uncompromising quality and client-first dedication.'
cp.about_story = 'Founded in 2023, Avail Technologies Pvt Ltd is a progressive software innovator, crafting bespoke digital solutions that redefine efficiency in African enterprises. We do not just build software, we pride ourselves in engineering growth.'
cp.contact_email = 'info@avail.co.zw'
cp.contact_phone = '+263 78 485 1863'
cp.office_address = 'Harare, Zimbabwe'
cp.save()
print('CompanyProfile updated.')


# 2. Services from Pamphlet
services_data = [
    {
        'title': 'General IT Consultation',
        'category_code': '01 / CONSULTING',
        'short_description': 'Clear, practical advice from experienced professionals who take the time to understand your goals and challenges.',
        'full_description': 'Our strategic technology consultants partner with your leadership to assess current systems, diagnose workflow bottlenecks, and recommend cost-effective, high-impact technology architectures.',
        'icon': 'fa-comments',
        'price_min': '150',
        'price_max': '450',
        'billing_period': '/ consultation scope',
        'price_min_annual': '1,200',
        'price_max_annual': '3,600',
        'pricing_model': 'Diagnostic Scope or Monthly Advisory Retainer',
        'turnkey_benefit': 'Actionable technology roadmaps that save capital and eliminate redundant licensing.',
        'deliverables_list': 'Comprehensive IT infrastructure and systems audit\nTechnology vendor assessment and contract review\nCost-benefit and operational ROI roadmap\nCloud vs on-premises architecture advisory',
        'commercial_terms': 'Dedicated senior consultant assigned\nWritten architectural evaluation report\nFollow-up review session included',
        'order': 1
    },
    {
        'title': 'Custom ERP Systems',
        'category_code': '02 / ENTERPRISE SOFTWARE',
        'short_description': 'Built around your workflow, not the other way around. No rigid templates, just intuitive, precision-crafted tools that feel like they were made for you.',
        'full_description': 'We architect and build tailored enterprise resource planning systems that mirror your specific operational procedures, integrating purchasing, inventory, warehousing, finance, and role-based permissions into a unified pane.',
        'icon': 'fa-sitemap',
        'price_min': '2,500',
        'price_max': '7,500',
        'billing_period': '/ module sprint',
        'price_min_annual': '24,000',
        'price_max_annual': '68,000',
        'pricing_model': 'Agile Milestone SOW or Dedicated Engineering Squad',
        'turnkey_benefit': 'Zero workflow compromises: an ERP tailored 100% to your African enterprise reality.',
        'deliverables_list': 'Tailored database schema and workflow automation\nCross-department operational modules (Stock, Finance, Logistics)\nGranular role-based security and audit trail logging\nReal-time executive analytics and reporting dashboards',
        'commercial_terms': 'Full IP and source code escrow options\n12-Month bug-fix warranty on custom modules\nStaff onboarding and administrator training',
        'order': 2
    },
    {
        'title': 'Web Development',
        'category_code': '03 / DIGITAL PLATFORMS',
        'short_description': 'From sleek portfolios to powerful enterprise platforms, we create websites that are as striking as they are performant, helping you stand out with confidence.',
        'full_description': 'We engineer high-performance web applications, customer portals, and corporate digital experiences following Apple-grade minimalist design principles, lightning-fast response times, and bulletproof security.',
        'icon': 'fa-globe',
        'price_min': '850',
        'price_max': '3,200',
        'billing_period': '/ project scope',
        'price_min_annual': '700',
        'price_max_annual': '2,600',
        'pricing_model': 'Fixed Project Milestone Scope',
        'turnkey_benefit': 'Blazing fast, responsive web platforms that turn visitors into enterprise clients.',
        'deliverables_list': 'Bespoke UI/UX design matching modern design standards\nClean, maintainable web architecture (Django, React, Node)\nMobile responsiveness and sub-second page loads\nSearch engine optimization (SEO) and security hardening',
        'commercial_terms': '60-Day post-launch support and bug fixing\nFull CMS handover and admin training session\nAutomated daily cloud backups included',
        'order': 3
    },
    {
        'title': 'Network Installation',
        'category_code': '04 / INFRASTRUCTURE',
        'short_description': 'We have a team of network technicians with decades of experience in setting up network infrastructures in different organisations of different sizes.',
        'full_description': 'Enterprise-grade structured cabling, rack staging, VLAN segmentation, and Wi-Fi coverage engineered specifically for high-throughput retail stores, depots, and corporate headquarters.',
        'icon': 'fa-network-wired',
        'price_min': '400',
        'price_max': '1,500',
        'billing_period': '/ site deployment',
        'price_min_annual': '3,500',
        'price_max_annual': '12,000',
        'pricing_model': 'Per Site Staging or Multi-Branch Rollout',
        'turnkey_benefit': 'Zero packet drop till-to-server latency with rock-solid physical cable runs.',
        'deliverables_list': 'Structured Cat6/Cat6A shielded copper cabling and trunking\nServer rack installation, patch panel termination and cable combs\nManaged PoE switches, VLAN configuration and firewall setup\nWi-Fi access point site survey and signal heat-mapping',
        'commercial_terms': 'Certified cable certification test reports\n5-Year structured cabling workmanship guarantee\nClean labelled patch panels and floor plan diagrams',
        'order': 4
    },
    {
        'title': 'Cyber Security Consultancy',
        'category_code': '05 / CYBER SECURITY',
        'short_description': 'We provide vulnerability testing for organisations from the information security perspective.',
        'full_description': 'Rigorous offensive security assessments, penetration testing, till network segmentation analysis, and security audits to safeguard your business from data breaches, ransomware, and insider threats.',
        'icon': 'fa-shield-halved',
        'price_min': '650',
        'price_max': '2,800',
        'billing_period': '/ assessment scope',
        'price_min_annual': '5,500',
        'price_max_annual': '22,000',
        'pricing_model': 'Vulnerability Audit Scope or Ongoing Security Retainer',
        'turnkey_benefit': 'Ironclad protection against cashier fraud, database breaches, and external intrusions.',
        'deliverables_list': 'External and internal vulnerability assessment\nTill network and POS endpoint security penetration testing\nAccess control, credential audit and policy review\nExecutive risk report with prioritized remediation steps',
        'commercial_terms': 'Non-disclosure agreement (NDA) signed upfront\nZero-downtime testing methodology\nComplimentary post-remediation verification scan',
        'order': 5
    },
    {
        'title': 'Fiscal Device & Compliance Integration',
        'category_code': '06 / COMPLIANCE',
        'short_description': 'Turnkey ZIMRA fiscalisation and statutory device integration for retail tills and wholesale depots.',
        'full_description': 'Direct hardware and cryptographic API integration with certified Electronic Signature Devices (ESD) and Fiscal Memory Devices, ensuring statutory tax compliance without checkout delays.',
        'icon': 'fa-file-invoice-dollar',
        'price_min': '250',
        'price_max': '850',
        'billing_period': '/ device model',
        'price_min_annual': '2,000',
        'price_max_annual': '6,800',
        'pricing_model': 'Per Device Certification or Enterprise Fleet License',
        'turnkey_benefit': '100% ZIMRA compliance with continuous offline signing buffer.',
        'deliverables_list': 'ZIMRA RevMax and ESD driver integration\nContinuous offline receipt signing and tamper-evident logging\nAutomated tax server telemetry and health alerts\nStatutory fiscal audit report generation',
        'commercial_terms': 'Full regulatory compliance guarantee\nFree updates for statutory tax rate adjustments\nOn-site technician assistance during tax inspector visits',
        'order': 6
    },
    {
        'title': '24/7 Managed Operations & Emergency SLA',
        'category_code': '07 / MANAGED OPERATIONS',
        'short_description': 'Round-the-clock enterprise support and emergency field technicians guaranteeing zero checkout downtime.',
        'full_description': 'Continuous proactive monitoring, remote diagnostics, on-site emergency dispatch, and guaranteed 15-minute response times for critical checkout incidents across your store footprint.',
        'icon': 'fa-headset',
        'price_min': '150',
        'price_max': '400',
        'billing_period': '/ store / mo',
        'price_min_annual': '1,400',
        'price_max_annual': '3,800',
        'pricing_model': 'Tiered SLA by Store Count and Trading Hours',
        'turnkey_benefit': 'Dedicated emergency standby technicians ensuring tills never stop ringing.',
        'deliverables_list': '24/7 dedicated telephone and WhatsApp hotline\nGuaranteed 15-minute critical incident response\nRemote health monitoring of till databases and hardware\nBuffer swap-out hardware available on standby',
        'commercial_terms': 'Service level agreement (SLA) with financial credits\nDedicated account engineer assigned\nMonthly operational performance and incident reports',
        'order': 7
    }
]

Service.objects.all().delete()
for s in services_data:
    Service.objects.create(**s)
print(f'Services populated: {Service.objects.count()} services.')

# 3. Hardware Products from Pamphlet
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

HardwareProduct.objects.all().delete()
for h in hardware_data:
    HardwareProduct.objects.create(**h)
print(f'Hardware products populated: {HardwareProduct.objects.count()} items.')
