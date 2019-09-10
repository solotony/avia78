# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import models

__author__ = 'solotony'


@login_required
def get_generickey_json(request):
    id = request.GET.get('id', None)
    if not id:
        raise Http404("id GET parameter")
    model_type = ContentType.objects.get_for_id(id)
    data = ContentType.get_all_objects_for_this_type(model_type)
    yy = ''
    for x in data:
        if yy:
            yy = yy + ','
        yy = yy+'{"model":"x","pk":"'+str(x.pk)+'","fields":{"title":"'+x.__str__()+'"}}'

    json = '['+yy+']'

    #json = serializers.serialize('json', yy)
    return HttpResponse(json, content_type='application/json')
