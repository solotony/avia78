from django.shortcuts import render, get_object_or_404
from .models import GalleryCategory, Photo
from django.core.paginator import Paginator

def categories(request):
    categories = GalleryCategory.objects.all()
    return render(request, 'gallery/categories.html', {
        'categories': categories,
        'menu': 'gallery'
    })

def _print_category(request, category):
    images_all = Photo.objects.filter(category=category).all()
    paginator = Paginator(images_all, 6)
    page_id = request.GET.get('page')
    paginator_page = paginator.get_page(page_id)
    return render(request, 'gallery/category.html', {
        'category': category,
        'images_all': paginator_page,
        'menu': 'gallery'
    })

def category(request, pk):
    category = get_object_or_404(GalleryCategory, pk=pk)
    return _print_category(request, category)

def category_by_slug(request, slug):
    category = get_object_or_404(GalleryCategory, slug=slug)
    return _print_category(request, category)
