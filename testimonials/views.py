from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Testimonial

def index(request):
    testimonials = Testimonial.objects.order_by('-id').all()
    #paginator = Paginator(testimonials, 6)
    #page_id = request.GET.get('page')
    #testimonials_page = paginator.get_page(page_id)
    return render(request, 'website/testimonial-index.html', {
        'testimonials': testimonials
    })

def testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    return render(request, 'website/testimonial-show.html', {
        'testimonial': testimonial
    })

