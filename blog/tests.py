from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Post

class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Architecture', slug='architecture')
        self.post = Post.objects.create(
            title='Why Offline Matters',
            slug='why-offline-matters',
            category=self.category,
            excerpt='Offline resilience article excerpt',
            content='Full markdown body of why offline matters in retail.',
            author_name='Avail Engineer',
            read_time_minutes=4,
            is_published=True,
        )

    def test_blog_list(self):
        response = self.client.get(reverse('blog:blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Why Offline Matters')

    def test_blog_search(self):
        response = self.client.get(reverse('blog:blog_list') + '?q=resilience')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Why Offline Matters')

    def test_blog_detail(self):
        response = self.client.get(reverse('blog:blog_detail', kwargs={'slug': 'why-offline-matters'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Why Offline Matters')
        self.assertContains(response, 'Avail Engineer')
        # View count should increment
        self.post.refresh_from_db()
        self.assertEqual(self.post.views_count, 1)
