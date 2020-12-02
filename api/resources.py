from tastypie.resources import ModelResource
from orders.models import Country

class CountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
