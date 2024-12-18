from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    id = models.BigAutoField(primary_key = True)
    code = models.CharField(unique=True, max_length=8)
    code3 = models.CharField(unique=True, max_length=8)
    name = models.CharField(max_length=64)
    tld = models.CharField(max_length=8)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Province(models.Model):
    id = models.BigAutoField(primary_key = True)
    name = models.CharField(max_length = 64)

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Regency(models.Model): # Kabupaten
    id = models.BigAutoField(primary_key = True)
    province = models.ForeignKey(Province, on_delete = models.PROTECT)
    name = models.CharField(max_length = 64)

    class Meta:
        verbose_name = _('Regency')
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model): # Kecamatan
    id = models.BigAutoField(primary_key = True)
    regency = models.ForeignKey(Regency, on_delete = models.PROTECT)
    name = models.CharField(max_length = 64)

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Village(models.Model): # Desa/Kelurahan
    id = models.BigAutoField(primary_key = True)
    district = models.ForeignKey(District, on_delete = models.PROTECT)
    name = models.CharField(max_length = 64)

    class Meta:
        verbose_name = _('Village')
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name



class BaseWorldMapModel(models.Model):
    province = models.ForeignKey(Province, verbose_name=_("Province"), on_delete = models.PROTECT, null = True, blank = True)
    regency = models.ForeignKey(Regency, verbose_name=_("Regency"), on_delete = models.PROTECT, null = True, blank = True)
    district = models.ForeignKey(District, verbose_name=_("District"), on_delete = models.PROTECT, null = True, blank = True)
    village = models.ForeignKey(Village, verbose_name=_("Village"), on_delete = models.PROTECT, null = True, blank = True)

    class Meta:
        abstract = True
