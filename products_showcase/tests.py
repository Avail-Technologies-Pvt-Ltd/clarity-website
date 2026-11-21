from django.test import TestCase, Client
from django.urls import reverse
from .models import ProductCategory, Product

class ProductShowcaseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ProductCategory.objects.create(name='Retail Solutions', slug='retail')
        self.product = Product.objects.create(
            category=self.category,
            name='Clarity Retail LAN',
            slug='clarity-retail-lan',
            badge='Offline-Ready Store POS',
            tagline='Fast touch POS',
            description='Detailed description of retail lan',
            architecture='In-Store Counter Engine',
            features_list='Offline mode | Keep sales moving | Works with zero internet\nDual Currency | Multi-tender checkout | USD and ZWG',
            minor_features='Counter: Suspended cart parking\nInventory: OEM cross-referencing',
            technical_specs='Hardware: Touch Till Station\nOS: Linux/Windows',
            icon='fa-cash-register',
            is_featured=True,
        )

    def test_product_list(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clarity Retail LAN')

    def test_product_list_filter(self):
        response = self.client.get(reverse('products:product_list') + '?category=retail')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clarity Retail LAN')

    def test_product_detail(self):
        response = self.client.get(reverse('products:product_detail', kwargs={'slug': 'clarity-retail-lan'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clarity Retail LAN')
        self.assertContains(response, 'Offline mode')
        self.assertContains(response, 'Suspended cart parking')
