from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from .models import Post, Category

def blog_list(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True).select_related('category')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        )

    featured_post = posts.filter(is_featured=True).first()
    if not featured_post and posts.exists() and not query and not category_slug:
        featured_post = posts.first()

    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'featured_post': featured_post,
        'categories': categories,
        'active_category': active_category,
        'query': query,
    })

def blog_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related('category'), slug=slug, is_published=True)
    
    # Increment views counter safely
    Post.objects.filter(id=post.id).update(views_count=F('views_count') + 1)
    post.refresh_from_db(fields=['views_count'])

    related_posts = Post.objects.filter(is_published=True).exclude(id=post.id)
    if post.category:
        category_posts = related_posts.filter(category=post.category)[:3]
        if category_posts.exists():
            related_posts = category_posts
        else:
            related_posts = related_posts[:3]
    else:
        related_posts = related_posts[:3]

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'related_posts': related_posts,
    })
