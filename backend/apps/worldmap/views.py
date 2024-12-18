from dal import autocomplete
from django.http import Http404
from apps.worldmap.models import *


class BaseQueryAC(autocomplete.Select2QuerySetView):

    def dispatch(self, request, *args, **kwargs):
        # for security, avoid direct access to autocomplete
        if not 'Sec-Fetch-Site' in request.headers:
            raise Http404()
        sfs = request.headers.get('Sec-Fetch-Site')
        if not sfs == 'same-origin':
            raise Http404()
        return super().dispatch(request, *args, **kwargs)



class BaseAutoComplete(BaseQueryAC):
    model = None
    owner_name = None
    model_field_name = None
    create_field = None

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.model.objects.none()
        qs = self.model.objects.all()
        if self.owner_name:
            owner_dict = self.forwarded
            if owner_dict:
                qs = qs.filter(**owner_dict)
        if self.q:
            qs = qs.filter(name__icontains = self.q)
        return qs


class CountryAutoComplete(BaseAutoComplete):
    model = Country


class ProvinceAutoComplete(BaseAutoComplete):
    model = Province


class RegencyAutoComplete(BaseAutoComplete):
    model = Regency
    owner_name = 'province'


class DistrictAutoComplete(BaseAutoComplete):
    model = District
    owner_name = 'regency'


class VillageAutoComplete(BaseAutoComplete):
    model = Village
    owner_name = 'district'
