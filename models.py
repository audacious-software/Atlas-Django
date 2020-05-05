from django.contrib.gis.db import models

class PostalCode(models.Model):
    objects = models.GeoManager()

    name = models.CharField(max_length=128)

    bounds = models.MultiPolygonField(blank=True, null=True)
    center = models.PointField(blank=True, null=True)
    country = models.CharField(max_length=2, default="us")

class TimeZone(models.Model):
    objects = models.GeoManager()

    name = models.CharField(max_length=256)
    bounds = models.MultiPolygonField(blank=True, null=True)


class Province(models.Model):
    objects = models.GeoManager()

    name = models.CharField(max_length=128)
    abbreviation = models.CharField(max_length=128, null=True, blank=True)

    bounds = models.MultiPolygonField(blank=True, null=True)
    center = models.PointField(blank=True, null=True)
    country = models.CharField(max_length=2, default="us")

class PhoneAreaCode(models.Model):
    objects = models.GeoManager()

    name = models.CharField(max_length=256)
    bounds = models.MultiPolygonField(blank=True, null=True)
    center = models.PointField(blank=True, null=True)
