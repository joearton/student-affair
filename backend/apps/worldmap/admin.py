from django.contrib import admin
from apps.worldmap.models import *


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'code', 'code3', 'tld')
    list_per_page = 15


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name')
    list_per_page = 15


@admin.register(Regency)
class RegencyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'province')
    list_filter = ['province']
    list_per_page = 15


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'regency')
    list_filter = ['regency__province']
    list_per_page = 15


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'district')
    list_filter = ['district__regency__province', 'district__regency']
    list_per_page = 15




