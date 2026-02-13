"""Views for the blog app."""
from django.shortcuts import render


def index(request):
    """View function for the home page of the site."""
    # Sample data structure - replace this with actual database queries
    sample_items = [
        {
            'title': 'Understanding the Basics of YAML',
            'description': 'A comprehensive guide to YAML syntax and usage.',
            'slug': 'yaml-basics',
            'banner': {
                'path': 'assets/drawing.svg'
            }
        }
    ]
    
    return render(request, "index.html", context={
        "items": sample_items,
        "cdn_url": "static/",
        "base_url": "/"
        })
