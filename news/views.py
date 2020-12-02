from django.shortcuts import render, get_object_or_404
from .models import *
from website.views import get_contact
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth, TruncYear
from django.db import connection

# Create your views here.

def index(request):
    posts = Post.objects.filter(published_at__gte='2011-10-29').order_by('-published_at')
    paginator = Paginator(posts, 6)
    page_id = request.GET.get('page')
    posts_page = paginator.get_page(page_id)

    #years = Post.objects.annotate(year=TruncYear('published_at')).aggregate().values('year').annotate(Count('pk'))

    truncate_date = connection.ops.date_trunc_sql('year', 'published_at')
    qs = Post.objects.filter(published_at__gte='2011-10-29').extra({'year': truncate_date})
    years = qs.values('year').annotate(Count('pk')).order_by('year')

    return render(request, 'website/news_list.html', {
        'posts': posts_page,
        'years': years,
    })

def digest_year(request, year):

    truncate_date = connection.ops.date_trunc_sql('month', 'published_at')
    qs = Post.objects.filter(published_at__gte='2011-10-29').filter(published_at__year=year).extra({'month': truncate_date})
    monthes = qs.values('month').annotate(Count('pk')).order_by('month')

    posts = Post.objects.filter(published_at__year=year).filter(published_at__gte='2011-10-29').order_by('published_at')
    return render(request, 'website/news_digest_year.html', {
        'posts': posts,
        'monthes':monthes,
        'year':year
    })

def digest_month(request, year, month):
    posts = Post.objects.filter(published_at__gte='2011-10-29').filter(published_at__year=year).filter(published_at__month=month).order_by('published_at')

    return render(request, 'website/news_digest_month.html', {
        'posts': posts,
        'month': month,
        'year': year
    })

def post_detail_ym(request, year, month, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'website/news_detail.html', {
        'post': post,
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'website/news_detail.html', {
        'post': post,
    })

def search(request):
    q = request.GET.get('q', '')
    name_map = {'id': 'id', 'published_at': 'published_at', 'slug': 'slug', 'search_data': 'search_data'}
    posts = Post.objects.raw("""
        SELECT `id`, `published_at`, `slug`, `search_data`, MATCH (`search_data`) AGAINST ( "%s" ) AS `score` 
        FROM `news_post` 
        WHERE MATCH (`search_data`) AGAINST ( "%s" ) 
        AND `published_at` > '2011-10-29'
        ORDER BY `score` DESC
        LIMIT 30
        """ % (q, q), translations=name_map)
    return render(request, 'website/search.html', {
        'query_string': q,
        'posts': posts
    })
