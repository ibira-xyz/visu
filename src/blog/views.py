"""Views for the blog app."""
from django.shortcuts import render


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
