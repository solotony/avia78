from django.shortcuts import render
from orders.models import Country, Price
from news.models import Post
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

def countries_from(request):
    countries = Country.objects.filter(b_from=True)
    data = serializers.serialize('json', countries)
    return HttpResponse(data, content_type="application/json")
    #return JsonResponse(countries, safe=False)

def countries_to(request):
    countries = Country.objects.filter(b_to=True)
    data = serializers.serialize('json', countries)
    return HttpResponse(data, content_type="application/json")

def prices(request):
    price = Price.objects.all()
    data = serializers.serialize('json', price)
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def search(request):
    #if request.is_ajax():
        if request.method == 'POST':
            data = json.loads(request.body.decode("utf-8"))
            #return JsonResponse(data)
            if not data["query"]:
                return HttpResponse('{"result":"error", "error":"Empty query", "query":}')
            q = data["query"]
            name_map = {'id': 'id', 'published_at': 'published_at', 'slug': 'slug', 'search_data': 'search_data'}
            posts = Post.objects.raw("""
                        SELECT `id`, `published_at`, `slug`, `search_data`, MATCH (`search_data`) AGAINST ( "%s" ) AS `score` 
                        FROM `news_post` 
                        WHERE MATCH (`search_data`) AGAINST ( "%s" ) 
                        AND `published_at` > '2011-10-29'
                        ORDER BY `score` DESC
                        LIMIT 3
                        """ % (q, q), translations=name_map)
            result = serializers.serialize('json', posts)
            return HttpResponse(result, content_type="application/json")

    #return HttpResponse('{"result":"error", "error":"Invalid Request"}')

