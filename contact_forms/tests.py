import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import ContactInquiry, DemoRequest, NewsletterSubscriber, MeetingBooking

class ContactFormsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_get(self):
        response = self.client.get(reverse('contact:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book a Consultation Meeting')
        self.assertContains(response, 'Avail Technologies (Pvt) Ltd')
        self.assertContains(response, 'info@avail.co.zw')
        # Verify personal details are removed
        self.assertNotContains(response, 'Tinashe Mphisa')
        self.assertNotContains(response, 'Francis E. Mawandu')

    def test_contact_submission(self):
        response = self.client.post(reverse('contact:contact'), {
            'name': 'Tatenda Zhou',
            'email': 'tatenda@autospares.co.zw',
            'phone': '+263771234567',
            'company': 'Harare Auto Spares',
            'meeting_topic': 'Clarity Retail LAN (Motor Spares POS & Offline Edge)',
            'meeting_format': 'google_meet',
            'preferred_date': '2026-12-01',
            'preferred_time_slot': 'Morning (09:00 - 11:00 CAT)',
            'store_count': '2-5',
            'notes': 'We have 4 spares branches and need offline counter POS.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MeetingBooking.objects.filter(email='tatenda@autospares.co.zw').exists())
        self.assertTrue(ContactInquiry.objects.filter(email='tatenda@autospares.co.zw').exists())

    def test_demo_request_redirect(self):
        # GET request_demo should redirect to the unified meeting booking page
        response = self.client.get(reverse('contact:request_demo'))
        self.assertEqual(response.status_code, 301)
        self.assertIn(reverse('contact:contact'), response.url)

    def test_demo_request_post(self):
        response = self.client.post(reverse('contact:request_demo'), {
            'name': 'Farai Moyo',
            'company_name': 'Premier Motor Parts',
            'email': 'farai@premierparts.co.zw',
            'phone': '+263772223344',
            'business_type': 'motor_spares_retail',
            'store_count': '2-5',
            'product_interest': 'Clarity Retail LAN',
            'preferred_timeframe': 'Immediately',
            'notes': 'Looking for auto parts counter system with part number search.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DemoRequest.objects.filter(company_name='Premier Motor Parts').exists())
        self.assertTrue(MeetingBooking.objects.filter(company_name='Premier Motor Parts').exists())

    def test_newsletter_subscribe(self):
        response = self.client.post(
            reverse('contact:newsletter_subscribe'),
            data=json.dumps({'email': 'subscriber@retail.com'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue(NewsletterSubscriber.objects.filter(email='subscriber@retail.com').exists())

