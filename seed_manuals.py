import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clarity_portal.settings')
django.setup()

from products_showcase.models import Product, ProductInstruction

manuals_data = [
    # ==========================================
    # CLARITY RETAIL LAN (Motor Spares Counter POS)
    # ==========================================
    {
        'product_slug': 'clarity-retail-lan',
        'section_number': '1.1',
        'title': 'Cashier Shift Start, Opening Float In & Hardware Checklist',
        'instruction_type': 'user_guide',
        'severity': 'info',
        'category': 'Daily Counter Operations',
        'summary': 'Protocol for counter operators opening a till shift, entering cash drawer float, and verifying receipt printer and barcode scanner responsiveness.',
        'detailed_content': (
            'At the start of every business day, counter operators must initialize their till session before serving customers. '
            'Clarity Retail LAN runs 100% autonomously on the local parts store server appliance. '
            'Even when city power fluctuations or internet uplinks fail, all till transactions, counter receipts, '
            'and cash ledger events are safely committed to the local database without latency.'
        ),
        'steps_list': (
            "Step 1: Power on the counter POS terminal and confirm the green network link LED is active on the local store server.\n"
            "Step 2: Enter your assigned Cashier PIN or scan your operator barcode badge to log in.\n"
            "Step 3: Select 'Open Till Shift' from the main counter navigation bar.\n"
            "Step 4: Count physical cash drawer float denominations (USD banknotes and local currency) and input values into the Float-In screen.\n"
            "Step 5: Tap 'Print Float Receipt' to confirm printer communication and verify the cash drawer kicks open automatically.\n"
            "Step 6: Test the handheld barcode scanner on a sample parts box to ensure rapid barcode decode."
        ),
        'warning_notes': (
            'Never begin counter sales without completing the Float-In step. Beginning shift trading with zero float '
            'creates unreconcilable discrepancy warnings during supervisor end-of-day Z-Report reconciliation.'
        ),
        'code_snippet': 'Hardware self-test: Press CTRL + ALT + P on the counter keyboard to trigger an instant ESC/POS printer line test.',
        'tags': 'float, counter, cashier, open shift, printer test, hardware checklist, auto parts'
    },
    {
        'product_slug': 'clarity-retail-lan',
        'section_number': '1.2',
        'title': 'Auto Parts Lookup, OEM Cross-Referencing & Shelf Bin Navigation',
        'instruction_type': 'user_guide',
        'severity': 'info',
        'category': 'Parts Catalog & Counter Search',
        'summary': 'How counter salesmen rapidly locate motor spares by vehicle make/model/year, OEM part numbers, aftermarket equivalents, and shelf bin aisle codes.',
        'detailed_content': (
            'Customer inquiries at an auto parts counter require immediate parts identification. '
            'Clarity Retail LAN provides a dedicated parts search engine that allows salesmen to query by OEM number, '
            'aftermarket manufacturer code (e.g. GMB, Bosch, Ferodo), or vehicle application (e.g. Toyota Hilux 1KD 2012 Brake Pads). '
            'The counter screen instantly displays live shelf stock, retail price, mechanic trade discount price, and exact bin location (e.g. Bin B-04-2).'
        ),
        'steps_list': (
            "Step 1: On the POS counter screen, press F2 or click the 'Part Search' field.\n"
            "Step 2: Type the part number, OEM reference, or vehicle description (e.g. 'D4D oil filter' or '04152-YZZA1').\n"
            "Step 3: Review matching results displaying on-hand shelf quantity, brand, and bin aisle location.\n"
            "Step 4: If the primary OEM brand is out of stock, click 'Cross References / Equivalents' to view compatible aftermarket alternatives.\n"
            "Step 5: Tap ENTER or double-click to add the item directly into the active sales ticket."
        ),
        'warning_notes': (
            'Always verify the vehicle engine code and manufacturing year before handing electrical sensors or brake discs to customers. '
            'Cross-check superseded part numbers shown in yellow badges to prevent customer returns.'
        ),
        'code_snippet': 'Quick Part Lookup shortcut: Press F2 from anywhere on the till screen to focus the part number search box.',
        'tags': 'part number, oem cross reference, bin location, vehicle search, brake pads, filters, spark plugs'
    },
    {
        'product_slug': 'clarity-retail-lan',
        'section_number': '2.1',
        'title': 'Generating Counter Quotations for Mechanics & Walk-In Customers',
        'instruction_type': 'user_guide',
        'severity': 'info',
        'category': 'Quotations & Invoicing',
        'summary': 'Procedure for preparing official written quotations for vehicle repairs, garage mechanics, and corporate fleet accounts.',
        'detailed_content': (
            'Car owners and mechanics frequently request written price quotations for insurance claims, fleet approvals, or vehicle servicing budgets. '
            'Clarity Retail LAN allows operators to build complete quotations with vehicle registration numbers, mechanic trade discounts, '
            'and dual-currency price totals. Quotations reserve shelf inventory for a configurable time window (e.g. 48 hours) without reducing ledger stock.'
        ),
        'steps_list': (
            "Step 1: Open the Counter Sales ticket and select 'New Quotation (F6)'.\n"
            "Step 2: Enter customer name, phone number, and vehicle registration number (e.g. ABC-1234).\n"
            "Step 3: If the customer is an accredited mechanic or fleet garage, select their account to apply negotiated trade discounts automatically.\n"
            "Step 4: Add all required replacement parts (suspension arms, bushings, gaskets, lubricants).\n"
            "Step 5: Click 'Print Quotation' to generate an A4 or 80mm itemized quote showing validity expiration date.\n"
            "Step 6: When the customer returns to purchase, retrieve the quote by number or phone search and click 'Convert to Fiscal Tax Invoice'."
        ),
        'warning_notes': (
            'Quotation prices are locked for 48 hours. If national exchange rates or wholesale supplier prices shift before the quote is converted to an invoice, '
            'supervisors must review and approve price overrides if validity has expired.'
        ),
        'code_snippet': 'Recall Quotation shortcut: Press F7 and scan or type quotation number to convert directly to checkout sale.',
        'tags': 'quotation, mechanic quote, fleet pricing, convert quote, auto parts estimate, vehicle reg'
    },
    {
        'product_slug': 'clarity-retail-lan',
        'section_number': '2.2',
        'title': 'Core Battery Deposit Returns & Defective Warranty Part Logging',
        'instruction_type': 'user_guide',
        'severity': 'caution',
        'category': 'Returns & Warranty',
        'summary': 'Standard operating procedure for processing old battery scrap returns (core deposits) and submitting defective warranty parts.',
        'detailed_content': (
            'Automotive retailers commonly charge a core deposit on lead-acid automotive batteries that is refunded when the customer '
            'returns their old scrap battery casing. Additionally, returned mechanical parts (alternators, starters, water pumps) '
            'under warranty require serial number verification and fault diagnostics logging before refunding or replacing.'
        ),
        'steps_list': (
            "Step 1: On the till screen, select 'Returns / Core Credits' from the options menu.\n"
            "Step 2: For battery scrap returns, select 'Battery Core Deposit Return' and inspect the physical battery casing for cracks or acid leaks.\n"
            "Step 3: Issue cash refund or apply core deposit credit toward the customer's new battery purchase.\n"
            "Step 4: For warranty claims, search original sales invoice number or scan serial number on defective part.\n"
            "Step 5: Enter defect description (e.g. 'no charge output on alternator') and technician diagnosis notes.\n"
            "Step 6: Print warranty intake slip and transfer part to the Warranty Return Holding Shelf."
        ),
        'warning_notes': (
            'Never accept physically damaged or cracked battery casings for scrap core refunds. '
            'All warranty returns must have matching serial numbers recorded on the original purchase receipt.'
        ),
        'tags': 'battery core, scrap return, warranty, defective part, alternator, credit note, refund'
    },
    {
        'product_slug': 'clarity-retail-lan',
        'section_number': '3.1',
        'title': 'Mandatory ZIMRA Fiscal Signature Device Interfacing on Counter Receipts',
        'instruction_type': 'warning_protocol',
        'severity': 'critical',
        'category': 'Fiscal Compliance & Law',
        'summary': 'Statutory legal operating protocol for certified Electronic Signature Devices (ESD) and fiscal memory counters.',
        'detailed_content': (
            'Statutory revenue regulations mandate that every commercial auto parts counter sale must be cryptographically signed '
            'by an approved fiscal device before the till receipt is issued to the customer. '
            'Clarity Retail LAN interfaces directly with certified fiscal hardware boxes via USB virtual COM, serial RS232, or network REST API. '
            'Every printed thermal receipt displays the official fiscal signature hash, ZIMRA tax counters, and QR verification code.'
        ),
        'steps_list': (
            "Step 1: Inspect the fiscal ESD hardware box on the counter and ensure the status LED shows steady GREEN ('ONLINE / FISCAL DAY OPEN').\n"
            "Step 2: Complete the counter sale in Clarity Retail LAN — the system automatically formats line items with tax categories (Standard 15%, Zero-Rated, Exempt).\n"
            "Step 3: The system transmits the fiscal invoice payload and waits for cryptographic signature confirmation.\n"
            "Step 4: Verify that the 80mm thermal receipt prints the statutory fiscal verification QR code and device signature hash at the bottom.\n"
            "Step 5: At close of business, run the mandatory fiscal End of Day Z-Report close."
        ),
        'warning_notes': (
            'CRITICAL STATUTORY WARNING: Never disconnect power or unplug data cables from the fiscal ESD box while an invoice is pending signature. '
            'Interrupting fiscal write cycles can corrupt hardware memory registers, resulting in system lockout and heavy statutory revenue authority penalties.'
        ),
        'code_snippet': 'Fiscal Status Check: Navigate to Till Settings > Fiscal Device Status (Expected: 200 OK "CERTIFIED_ACTIVE")',
        'tags': 'fiscal, zimra, esd, tax invoice, qr code, z-report, statutory compliance, penalty'
    },
    {
        'product_slug': 'clarity-retail-lan',
        'section_number': '3.2',
        'title': 'Midday Cash Drops, Supervisor Overrides & Shift Z-Report Closing',
        'instruction_type': 'admin_manual',
        'severity': 'warning',
        'category': 'Cash Management & Security',
        'summary': 'Supervised procedures for midday cashier drawer skims, supervisor PIN overrides, and end-of-day discrepancy reporting.',
        'detailed_content': (
            'To minimize security risk and cash exposure at the sales counter, store managers must enforce blind cash drops '
            'whenever cash drawer balances exceed store threshold limits ($500 or equivalent local currency). '
            'In blind cash drops, cashiers count and drop currency into security envelopes without seeing expected system totals.'
        ),
        'steps_list': (
            "Step 1: When the system notifies 'Drawer Cash Threshold Exceeded', the operator calls the store supervisor.\n"
            "Step 2: Select 'Blind Cash Drop / Skim' from the Till Operations menu.\n"
            "Step 3: The cashier counts banknotes to drop, places them in a tamper-evident drop envelope, and enters physical count.\n"
            "Step 4: The supervisor enters their PIN or scans supervisor RFID card to countersign the drop voucher.\n"
            "Step 5: Deposit the sealed envelope into the store time-delayed drop safe.\n"
            "Step 6: At the end of the shift, perform 'Close Shift', print cashier X-Report, reconcile counted cash, and generate final Z-Report."
        ),
        'warning_notes': (
            'Under no circumstances should supervisors reveal real-time POS cash expected totals to cashiers prior to cash counting. '
            'Blind counting prevents cashier manipulation of tender slips to conceal register shortages.'
        ),
        'tags': 'cash drop, drawer skim, supervisor override, theft prevention, z-report, shift close'
    },

    # ==========================================
    # CLARITY WHOLESALE LAN (Auto Parts Depot)
    # ==========================================
    {
        'product_slug': 'clarity-wholesale-lan',
        'section_number': '1.1',
        'title': 'Shipping Container Receiving & Bulk Auto Parts Barcode Verification',
        'instruction_type': 'user_guide',
        'severity': 'info',
        'category': 'Warehouse Depot Inbound',
        'summary': 'How warehouse receiving clerks scan import container manifests, match purchase orders, and accept parts into depot quarantine bays.',
        'detailed_content': (
            'Clarity Wholesale LAN accelerates inbound intake for auto parts importers and bulk distributors receiving 20ft/40ft shipping containers. '
            'Inbound parts cartons are scanned using rugged wireless barcode scanners to verify master carton counts, part numbers, '
            'and supplier shipment manifests against original purchase orders before releasing stock for sale.'
        ),
        'steps_list': (
            "Step 1: Open Clarity Wholesale LAN > Inbound Logistics > New Goods Receiving Voucher (GRV).\n"
            "Step 2: Select the Supplier Purchase Order number or scan Supplier Container Bill of Lading.\n"
            "Step 3: Use the wireless barcode scanner to scan each incoming master carton barcode (e.g. 10x Shock Absorbers per carton).\n"
            "Step 4: Verify part numbers, quantities, and inspect packaging for transit damage.\n"
            "Step 5: Click 'Commit Goods to Receiving Bay' and print pallet destination bin tags (e.g. Rack C, Shelf 3)."
        ),
        'warning_notes': (
            'Never commit a goods receipt voucher with mismatched part numbers or missing carton counts. '
            'Discrepancies must be flagged as "Shortage on Delivery" before container release to ensure shipping insurance claims are honored.'
        ),
        'code_snippet': 'Depot Handheld Scanner Pairing: Scan pairing barcode from Settings > Wireless Scanners to link terminal.',
        'tags': 'grv, goods receiving, shipping container, barcode scanner, warehouse, pallet, parts intake'
    },
    {
        'product_slug': 'clarity-wholesale-lan',
        'section_number': '1.2',
        'title': 'Multi-Tier Mechanic, Garage & Reseller Pricing Profiles',
        'instruction_type': 'admin_manual',
        'severity': 'info',
        'category': 'Wholesale Pricing & Accounts',
        'summary': 'Configuring differential pricing tiers for commercial workshops, panel beaters, municipal fleets, and retail spares shops.',
        'detailed_content': (
            'Wholesale auto parts distributors serve diverse commercial clients who buy on different pricing structures. '
            'Clarity Wholesale LAN enables depot managers to define customer price tiers (e.g. Tier 1: Retail Spares Shops, '
            'Tier 2: Certified Fleet Workshops, Tier 3: Walk-In Independent Mechanics) and assign credit limits with strict payment term enforcement.'
        ),
        'steps_list': (
            "Step 1: Navigate to Customers > Commercial Accounts > Select Account Profile.\n"
            "Step 2: Assign Price Tier (Tier A / Wholesale Importer Cost + 12%, Tier B / Garage Trade Cost + 20%, Tier C / Counter Standard).\n"
            "Step 3: Set Approved Credit Limit (e.g. $10,000 USD) and Payment Terms (e.g. 30 Days End of Month).\n"
            "Step 4: Configure Authorized Order Requisitioners and delivery address profiles.\n"
            "Step 5: Click 'Save Account Policy'. Invoicing staff will now automatically see locked contracted rates."
        ),
        'warning_notes': (
            'The system automatically halts invoice generation if an account has overdue 30-day balances exceeding approved credit limits. '
            'Credit limit bypass requires written director authorization and supervisor credential override.'
        ),
        'tags': 'price tiers, wholesale pricing, credit control, mechanic discounts, commercial garage'
    },
    {
        'product_slug': 'clarity-wholesale-lan',
        'section_number': '2.1',
        'title': 'Depot Picking Slip Generation & Bin Aisle Route Optimization',
        'instruction_type': 'user_guide',
        'severity': 'info',
        'category': 'Fulfillment & Order Picking',
        'summary': 'Generating scannable picking lists sorted by warehouse aisle and shelf bin sequence to maximize order assembly speed.',
        'detailed_content': (
            'When large orders are received from regional spares retailers or commercial bus companies, picking efficiency is critical. '
            'Clarity Wholesale LAN converts approved sales orders into optimized warehouse picking slips, grouping items '
            'by depot aisle sequence (e.g. Aisle 1 Engine Parts -> Aisle 2 Suspension -> Aisle 3 Electrical) to eliminate picker backtracking.'
        ),
        'steps_list': (
            "Step 1: Go to Orders > Pending Fulfillment > Select Approved Sales Order.\n"
            "Step 2: Click 'Generate Optimized Picking Slip'.\n"
            "Step 3: Print physical picking slip or dispatch order directly to warehouse picker handheld terminal.\n"
            "Step 4: Picker navigates aisles following bin location order and scans each item barcode to confirm picking accuracy.\n"
            "Step 5: Bring picked items to dispatch staging bench for packing inspection."
        ),
        'warning_notes': (
            'Picking errors on auto parts (e.g. picking a left-hand tie rod end instead of right-hand) lead to costly return logistics. '
            'Always scan the part barcode on the shelf rather than typing codes manually.'
        ),
        'tags': 'picking slip, warehouse, bin route, fulfillment, auto parts depot, barcode pick'
    },
    {
        'product_slug': 'clarity-wholesale-lan',
        'section_number': '2.2',
        'title': 'Commercial A4 Tax Invoicing & Trade Credit Limit Enforcement',
        'instruction_type': 'admin_manual',
        'severity': 'caution',
        'category': 'Billing & Invoicing',
        'summary': 'Generating statutory multi-currency commercial A4 tax invoices with delivery note cross-references, bank details, and VAT compliance.',
        'detailed_content': (
            'Commercial auto parts wholesale requires formal A4 multi-currency tax invoices for accounting and tax audits. '
            'Clarity Wholesale LAN prints comprehensive A4 invoices displaying detailed part descriptions, vehicle applications, '
            'OEM codes, bank payment instructions (Nostro USD and local currency), and statutory fiscal signature verification.'
        ),
        'steps_list': (
            "Step 1: In Sales Orders, verify that all picked items have been verified by the warehouse dispatcher.\n"
            "Step 2: Click 'Generate Commercial Tax Invoice'.\n"
            "Step 3: Verify customer billing details, PO reference number, and delivery address.\n"
            "Step 4: Select currency settlement method (USD Bank Transfer, Nostro, Cash, or Approved Credit).\n"
            "Step 5: Print 3 copies of A4 Commercial Invoice: Customer Original, Gate Security Pass, and Accounting File copy."
        ),
        'warning_notes': (
            'Commercial tax invoices cannot be modified once printed and signed by the fiscal memory module. '
            'Any returns or corrections must be processed through a formal Credit Note voucher referencing the original invoice number.'
        ),
        'tags': 'a4 invoice, commercial tax invoice, trade credit, billing, wholesale billing, vat'
    },
    {
        'product_slug': 'clarity-wholesale-lan',
        'section_number': '3.1',
        'title': 'Scannable Delivery Waybills & Transporter Dispatch Manifests',
        'instruction_type': 'user_guide',
        'severity': 'caution',
        'category': 'Dispatch & Transporter Logistics',
        'summary': 'Creating tamper-evident scannable carton labels and delivery van manifests for driver handoff and proof-of-delivery.',
        'detailed_content': (
            'Wholesale auto parts dispatched to retail shops or out-of-town workshops require rigorous chain-of-custody tracking. '
            'Clarity Wholesale LAN prints 4x6 inch thermal shipping labels with scannable waybill barcodes. '
            'When the delivery van driver arrives, scanning the waybill barcode transfers custody from the warehouse to the driver manifest.'
        ),
        'steps_list': (
            "Step 1: Navigate to Dispatch Staging > Orders Ready for Delivery.\n"
            "Step 2: Verify packed carton count and click 'Print Scannable Waybill Label'.\n"
            "Step 3: Adhere thermal 4x6 label firmly to the outer shipping box or wrapped parts pallet.\n"
            "Step 4: When delivery driver arrives, select 'Dispatch to Transporter / Van'.\n"
            "Step 5: Driver scans the waybill barcode with mobile terminal or signs the physical delivery manifest.\n"
            "Step 6: Security gate verifies manifest barcode before allowing delivery vehicle to exit depot."
        ),
        'warning_notes': (
            'Never release high-value automotive parts (turbochargers, ECUs, complete gearboxes) without a signed driver waybill. '
            'Unsigned dispatches void transit insurance in case of road accidents or delivery shortages.'
        ),
        'tags': 'waybill, delivery van, dispatch, transporter, scannable label, custody transfer, proof of delivery'
    },

    # ==========================================
    # HOSTEL MANAGEMENT SYSTEM
    # ==========================================
    {
        'product_slug': 'hostel-management-system',
        'section_number': '1.1',
        'title': 'Student Intake, Room & Bed Allocation Protocol',
        'instruction_type': 'user_guide',
        'severity': 'info',
        'category': 'Student Registration & Rooms',
        'summary': 'Procedure for enrolling students, assigning rooms and beds on visual floor plans, and issuing digital room keys.',
        'detailed_content': (
            'At the start of every academic semester, hostel wardens manage high volumes of student check-ins. '
            'Hostel Management System provides a live visual floor plan showing single, twin, and quad-sharing room occupancy. '
            'Wardens can immediately allocate verified students to specific bed spaces while preventing double-bookings.'
        ),
        'steps_list': (
            "Step 1: Open Hostel Management System > Students > New Registration.\n"
            "Step 2: Enter student name, national ID, university registration number, and emergency guardian contact.\n"
            "Step 3: Open 'Visual Room Matrix' to view available beds in Block A, B, or C.\n"
            "Step 4: Select vacant bed and click 'Allocate Bed Space'.\n"
            "Step 5: Record room inventory condition checklist (mattress, study desk, wardrobe key, window lock).\n"
            "Step 6: Print Resident Check-In Agreement and issue digital hostel gate pass."
        ),
        'warning_notes': (
            'Always inspect and record existing room damages on the intake checklist before handing room keys to students. '
            'Undocumented room damage cannot be deducted from student security deposits at semester check-out.'
        ),
        'tags': 'student intake, room allocation, bed matrix, hostel warden, check in, key handover'
    },
    {
        'product_slug': 'hostel-management-system',
        'section_number': '1.2',
        'title': 'Semester Rental Invoicing & Mobile Payment Reconciliation',
        'instruction_type': 'admin_manual',
        'severity': 'caution',
        'category': 'Rent Billing & Payments',
        'summary': 'Generating semester boarding invoices, recording bank transfers and mobile payments, and tracking arrears.',
        'detailed_content': (
            'Hostel finance officers require clear visibility over tuition and accommodation fee payments. '
            'The system generates semester rental invoices, applies security deposit fees, and logs payments across '
            'multiple payment channels (EcoCash, Innbucks, Nostro bank transfers, and cash). '
            'Automated SMS/email statements notify parents and students of upcoming fee deadlines.'
        ),
        'steps_list': (
            "Step 1: Navigate to Billing > Semester Invoicing > Generate Batch Invoices.\n"
            "Step 2: Select academic term (e.g. Semester 1 - 2026) and room rate plan.\n"
            "Step 3: When a payment is received, open Payments > Record Payment.\n"
            "Step 4: Enter payment reference code, bank name, or mobile money transaction ID.\n"
            "Step 5: The system automatically matches payment to student account and updates balance.\n"
            "Step 6: Print official hostel receipt or send WhatsApp payment confirmation."
        ),
        'warning_notes': (
            'Do not allocate room keys to students without minimum deposit threshold clearance. '
            'Enforcing clear payment rules at check-in eliminates mid-semester arrears disputes.'
        ),
        'tags': 'rent billing, hostel fees, mobile money, ecocash, arrears, student payments, receipt'
    },

    # ==========================================
    # EVENT MANAGEMENT SYSTEM
    # ==========================================
    {
        'product_slug': 'event-management-system',
        'section_number': '1.1',
        'title': 'High-Speed QR Ticket Door Validation & Gate LAN Turnstiles',
        'instruction_type': 'user_guide',
        'severity': 'info',
        'category': 'Gate Check-In & Turnstiles',
        'summary': 'Operating handheld barcode scanners and gate tablets to validate tickets in under 1 second without internet.',
        'detailed_content': (
            'Conferences, trade exhibitions, and concert gates experience intense attendee arrival spikes. '
            'Event Management System operates on a local gate LAN server so that ticket verification takes less than 1 second per attendee, '
            'even if mobile cellular towers are overwhelmed by crowd density. Scanned tickets are synchronized instantly across all gate turnstiles '
            'to completely prevent ticket sharing or duplicate re-entry.'
        ),
        'steps_list': (
            "Step 1: Power on gate validation smartphones or handheld 2D QR scanners connected to the gate Wi-Fi router.\n"
            "Step 2: Open Event Gate Check-In app and select the active event session.\n"
            "Step 3: Scan the attendee digital ticket QR code displayed on their phone screen or printed paper ticket.\n"
            "Step 4: The screen flashes GREEN ('VALID - ACCESS GRANTED') and displays attendee name and ticket tier (VIP, Delegate, General).\n"
            "Step 5: If a ticket is scanned a second time at another turnstile, the screen flashes RED with an audible alarm ('DUPLICATE SCAN DETECTED')."
        ),
        'warning_notes': (
            'Ensure all gate validation devices are connected to the local Event Gate LAN before attendees arrive. '
            'A detached gate terminal running in isolated standalone mode cannot check for duplicate scans occurring at other entrance doors.'
        ),
        'code_snippet': 'Gate Terminal Test: Scan admin calibration barcode to test scanner beep and gate turnstile relay trigger.',
        'tags': 'qr ticket, turnstile, gate check in, door access, duplicate prevention, conference, concert'
    },
    {
        'product_slug': 'event-management-system',
        'section_number': '1.2',
        'title': 'On-Site Attendee Registration & Instant Badge Lanyard Printing',
        'instruction_type': 'admin_manual',
        'severity': 'info',
        'category': 'Badge Printing & Registration',
        'summary': 'Procedure for registering walk-in VIPs and delegates and printing personalized conference badges at registration desks.',
        'detailed_content': (
            'Trade exhibitions, summits, and symposiums require on-demand badge printing for pre-registered attendees and walk-in VIPs. '
            'The system connects directly to direct thermal badge printers to generate customized attendee credentials with attendee name, '
            'company, country flag, and personalized door access QR code in under 5 seconds.'
        ),
        'steps_list': (
            "Step 1: At registration desk, search attendee by surname, email, or company name.\n"
            "Step 2: For walk-in registrations, click 'New Walk-In Delegate' and capture contact details and delegate fee payment.\n"
            "Step 3: Click 'Print Attendee Badge' — the system transmits print commands to the connected color badge printer.\n"
            "Step 4: Slip the printed PVC or card badge into the conference lanyard holder and hand to delegate.\n"
            "Step 5: The attendee's profile is immediately active across all session tracking turnstiles."
        ),
        'warning_notes': (
            'Keep spare rolls of badge stock and replacement thermal transfer ribbons at every registration station. '
            'Changing badge media mid-registration rush causes unnecessary attendee queues.'
        ),
        'tags': 'badge printing, conference lanyard, delegate registration, vip pass, exhibition desk'
    }
]

# Wipe old and insert clean
ProductInstruction.objects.all().delete()
print("Cleared existing instruction records.")

inserted = 0
for item in manuals_data:
    try:
        prod = Product.objects.get(slug=item['product_slug'])
        inst = ProductInstruction.objects.create(
            product=prod,
            section_number=item['section_number'],
            title=item['title'],
            instruction_type=item['instruction_type'],
            severity=item['severity'],
            category=item['category'],
            summary=item['summary'],
            detailed_content=item['detailed_content'],
            steps_list=item['steps_list'],
            warning_notes=item['warning_notes'],
            code_snippet=item.get('code_snippet', ''),
            tags=item['tags'],
            is_active=True,
        )
        inserted += 1
        print(f"[{prod.slug}] Added §{inst.section_number}: {inst.title}")
    except Product.DoesNotExist:
        print(f"Product slug '{item['product_slug']}' not found in DB! Skipping.")

print(f"\nSUCCESS: Inserted {inserted} professional user manual topics into database.")
