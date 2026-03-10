"""Views for the blog app."""
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import Post
from .processors.content_parser import ContentParser

def index(request):
    """View function for the home page of the site."""
    # Sample data structure - replace this with actual database queries
    sample_items = Post.objects.all()[:10]  # Fetch the latest 10 posts from the database

    return render(request, "index.html", context={
        "items": sample_items,
        "cdn_url": "static/",
        "cms_url": "https://cdn.ibira.xyz/",
        "base_url": "/"
        })

def post_detail(request, slug):
    """View function for the detail page of a single post."""
    try:
        post = Post.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return render(request, "not_found.html", status=404)

    parser = ContentParser(post.content, "https://cdn.ibira.xyz/")
    html_content = parser.parse()

    return render(request, "post.html", context={
        "post": post,
        "content": html_content,
        "component_scripts":  parser.component_scripts,
        "cdn_url": "static/",
        "cms_url": "https://cdn.ibira.xyz/",
        "base_url": "/"
        })
