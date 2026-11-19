import json
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import ContactInquiry, DemoRequest, NewsletterSubscriber, MeetingBooking

def contact_page(request):
    product_slug = request.GET.get('product') or request.GET.get('item') or request.GET.get('topic') or ''
    inquiry_param = request.GET.get('inquiry', '')
    tier_param = request.GET.get('tier', '')
    branches_param = request.GET.get('branches', '')
    tills_param = request.GET.get('tills', '')
    users_param = request.GET.get('users', '')
    type_param = request.GET.get('type', '')

    product_map = {
        'clarity-retail-lan': 'Clarity Retail LAN (Motor Spares POS & Offline Edge)',
        'clarity-wholesale-lan': 'Clarity Wholesale LAN (Auto Parts Depots & Distribution)',
        'single-till-retail-lan': 'Clarity Retail LAN (Motor Spares POS & Offline Edge)',
        'multi-till-retail-store': 'Clarity Retail LAN (Motor Spares POS & Offline Edge)',
        'wholesale-depot-lan': 'Clarity Wholesale LAN (Auto Parts Depots & Distribution)',
        'enterprise-multi-branch-lan': 'Custom Enterprise Software & ERP Bridge Engineering',
        'hostel-management-system': 'Student Hostel Management Platform',
        'event-management-system': 'Event Management Platform',
        'turnkey_kit': 'Turnkey POS Hardware & Appliance Staging Kits',
        'hardware': 'Turnkey POS Hardware & Appliance Staging Kits',
        'pos-printers': 'POS Thermal Receipt Printers & Till Hardware',
        'a4-printers': 'Commercial Laser & A4 Invoicing Printers',
        'barcode-readers': 'Rugged Optical Barcode Readers & Scanners',
        'laptops': 'Heavy-Duty Counter POS Laptops & Workstations',
        'network-equipment-cables': 'Shielded Gigabit Cabling & Managed Switches',
    }

    if type_param == 'wholesale':
        initial_topic = 'Clarity Wholesale LAN (Auto Parts Depots & Distribution)'
    else:
        initial_topic = product_map.get(product_slug) or product_map.get(tier_param) or product_map.get(inquiry_param) or 'Clarity Retail LAN (Motor Spares POS & Offline Edge)'

    # Build helpful pre-filled notes if arriving from LAN sizing calculator or tier card
    prefill_notes_parts = []
    if tier_param:
        prefill_notes_parts.append(f"Selected Plan: {tier_param}")
    if branches_param or tills_param or users_param:
        scale_str = []
        if branches_param:
            scale_str.append(f"{branches_param} Branch(es)")
        if tills_param:
            scale_str.append(f"{tills_param} Till(s)")
        if users_param:
            scale_str.append(f"{users_param} Active User(s)")
        prefill_notes_parts.append(f"Operational Scale: {', '.join(scale_str)}")

    prefill_notes = " | ".join(prefill_notes_parts) if prefill_notes_parts else ""

    # Map branches parameter to store_count select
    initial_store_count = "1"
    if branches_param:
        try:
            b_val = int(branches_param)
            if b_val == 1:
                initial_store_count = "1"
            elif 2 <= b_val <= 5:
                initial_store_count = "2-5"
            elif 6 <= b_val <= 20:
                initial_store_count = "6-20"
            else:
                initial_store_count = "20+"
        except ValueError:
            initial_store_count = "1"

    # Default suggested booking date: next business day
    tomorrow = date.today() + timedelta(days=1)
    if tomorrow.weekday() >= 5:
        tomorrow += timedelta(days=(7 - tomorrow.weekday()))
    min_date = date.today().strftime('%Y-%m-%d')
    suggested_date = tomorrow.strftime('%Y-%m-%d')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company = request.POST.get('company', '').strip() or request.POST.get('company_name', '').strip()
        meeting_topic = request.POST.get('meeting_topic', '').strip() or request.POST.get('inquiry_type', initial_topic).strip()
        meeting_format = request.POST.get('meeting_format', 'google_meet').strip()
        preferred_date_str = request.POST.get('preferred_date', '').strip()
        preferred_time_slot = request.POST.get('preferred_time_slot', 'Morning (09:00 - 11:00 CAT)').strip()
        store_count = request.POST.get('store_count', '1').strip()
        notes = request.POST.get('notes', '').strip() or request.POST.get('message', '').strip()

        if not name or not email or not phone or not company:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please provide your Full Name, Business Email, Phone/WhatsApp, and Company Name.'
                }, status=400)
            messages.error(request, 'Please provide all required fields (Name, Email, Phone, Company).')
            return render(request, 'contact_forms/contact.html', {
                'initial_topic': initial_topic,
                'min_date': min_date,
                'suggested_date': suggested_date,
                'prefill_notes': prefill_notes,
                'initial_store_count': initial_store_count,
            })

        parsed_date = None
        if preferred_date_str:
            try:
                parsed_date = date.fromisoformat(preferred_date_str)
            except ValueError:
                parsed_date = None

        booking = MeetingBooking.objects.create(
            name=name,
            email=email,
            phone=phone,
            company_name=company,
            meeting_topic=meeting_topic,
            meeting_format=meeting_format,
            preferred_date=parsed_date,
            preferred_time_slot=preferred_time_slot,
            store_count=store_count,
            notes=notes,
        )

        # Also store inquiry record for backwards compatibility
        ContactInquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=company,
            inquiry_type='demo',
            message=f"Meeting Booked: {meeting_topic} via {booking.get_meeting_format_display()} on {preferred_date_str} ({preferred_time_slot}). Store count: {store_count}. Notes: {notes}",
        )

        success_msg = f"Thank you, {name}! Your consultation meeting for {company} has been reserved. Our engineering lead will send calendar invitations and contact you via WhatsApp/Phone ({phone}) to confirm."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': success_msg,
                'booking_id': booking.id,
            })

        messages.success(request, success_msg)
        return redirect('contact:contact')

    return render(request, 'contact_forms/contact.html', {
        'initial_topic': initial_topic,
        'min_date': min_date,
        'suggested_date': suggested_date,
        'prefill_notes': prefill_notes,
        'initial_store_count': initial_store_count,
    })


def request_demo_page(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company_name = request.POST.get('company_name', '').strip() or request.POST.get('company', '').strip()
        business_type = request.POST.get('business_type', 'motor_spares_retail').strip()
        store_count = request.POST.get('store_count', '1').strip()
        product_interest = request.POST.get('product_interest', 'Clarity Retail LAN').strip()
        preferred_timeframe = request.POST.get('preferred_timeframe', 'This Week').strip()
        notes = request.POST.get('notes', '').strip()

        if name and email:
            DemoRequest.objects.create(
                name=name,
                email=email,
                phone=phone,
                company_name=company_name,
                business_type=business_type,
                store_count=store_count,
                product_interest=product_interest,
                preferred_timeframe=preferred_timeframe,
                notes=notes,
            )
            MeetingBooking.objects.create(
                name=name,
                email=email,
                phone=phone,
                company_name=company_name,
                meeting_topic=product_interest,
                meeting_format='google_meet',
                store_count=store_count,
                notes=notes,
            )
        success_msg = f"Thank you, {name}! Your consultation meeting request has been received."
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': success_msg})
        messages.success(request, success_msg)
        return redirect('contact:contact')

    # If GET, redirect to unified meeting booking page
    query = request.META.get('QUERY_STRING', '')
    url = reverse('contact:contact')
    if query:
        url += f"?{query}"
    return redirect(url, permanent=True)



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def newsletter_subscribe(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email', '').strip()
        else:
            email = request.POST.get('email', '').strip()

        if not email or '@' not in email:
            return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'}, status=400)

        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            return JsonResponse({'status': 'success', 'message': 'Welcome aboard! You have successfully subscribed to Clarity insights.'})
        else:
            return JsonResponse({'status': 'info', 'message': 'You are already subscribed to our newsletter.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
