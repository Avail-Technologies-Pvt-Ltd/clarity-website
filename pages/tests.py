from django.test import TestCase, Client
from django.urls import reverse
from products_showcase.models import ProductCategory, Product
from pages.models import Service, PricingPlan, Capability, FAQItem, CompanyMetric

class PagesViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ProductCategory.objects.create(name='Retail', slug='retail')
        self.product = Product.objects.create(
            category=self.category,
            name='Clarity Retail LAN',
            slug='clarity-retail-lan',
            badge='POS',
            tagline='Fast POS',
            description='Test POS description',
            architecture='LAN',
            features_list='Feature 1 | Detail 1',
            technical_specs='Spec: Val',
            icon='fa-cash-register',
            is_featured=True,
        )
        self.capability = Capability.objects.create(
            pillar_number='Pillar 01',
            title='Autonomous Edge & Offline-First Systems',
            slug='edge-systems',
            short_summary='Offline edge architecture',
            full_description='Full description of offline edge architecture',
            icon='fa-server',
            technical_bullets='Bullet 1\nBullet 2',
            bento_span=8,
            order=1,
            is_active=True,
        )
        self.service = Service.objects.create(
            title='Custom Enterprise Software Engineering',
            slug='custom-engineering',
            category_code='01 / CUSTOM ENGINEERING',
            short_description='Custom software description',
            full_description='Full service description',
            icon='fa-code',
            deliverables_list='Deliverable 1\nDeliverable 2',
            order=1,
            is_featured=True,
            is_active=True,
        )
        self.plan1 = PricingPlan.objects.create(
            name='Starter Store',
            slug='starter-store',
            plan_type='software',
            price_amount='49',
            billing_period='/ store / mo',
            features_list='Feature 1\nFeature 2',
            order=1,
            is_active=True,
        )
        self.plan2 = PricingPlan.objects.create(
            name='Growth Chain',
            slug='growth-chain',
            plan_type='software',
            price_amount='149',
            billing_period='/ chain / mo',
            features_list='Feature 1\nFeature 2',
            badge='Most Popular',
            is_featured=True,
            order=2,
            is_active=True,
        )

    def test_home_page(self):
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Avail Technologies')
        self.assertContains(response, 'What We Do')
        self.assertContains(response, 'Clarity Retail LAN')
        self.assertContains(response, 'Professional Implementation &amp; Support')

    def test_what_we_do_page(self):
        response = self.client.get(reverse('pages:what_we_do'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'What We Do')
        self.assertContains(response, 'Autonomous Edge')

    def test_services_page(self):
        response = self.client.get(reverse('pages:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Professional Services')
        self.assertContains(response, 'Custom Enterprise Software Engineering')

    def test_pricing_page(self):
        response = self.client.get(reverse('pages:pricing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Commercial Software Licensing')
        self.assertContains(response, 'Transparent Pricing')

    def test_about_page(self):
        response = self.client.get(reverse('pages:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Avail Technologies')

    def test_faq_page(self):
        response = self.client.get(reverse('pages:faq'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Frequently Asked Questions')
