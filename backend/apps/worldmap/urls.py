from apps.worldmap.views import (
    CountryAutoComplete, ProvinceAutoComplete,
    RegencyAutoComplete, DistrictAutoComplete,
    VillageAutoComplete, autocomplete
)
from django.urls import path

urlpatterns = [
    path('ac/country', CountryAutoComplete.as_view(), name='ac.worldmap.country'),
    path('ac/province', ProvinceAutoComplete.as_view(), name='ac.worldmap.province'),
    path('ac/regency', RegencyAutoComplete.as_view(), name='ac.worldmap.regency'),
    path('ac/district', DistrictAutoComplete.as_view(), name='ac.worldmap.district'),
    path('ac/village', VillageAutoComplete.as_view(), name='ac.worldmap.village'),
]
