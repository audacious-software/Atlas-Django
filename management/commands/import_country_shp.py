from __future__ import print_function
from builtins import str
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from atlas.models import Country

class Command(BaseCommand):
    help = 'Imports boundaries from shapefile files.'

    def add_arguments(self, parser):
        parser.add_argument('source', type=str)

    def handle(self, *args, **options):
        data_source = DataSource(options['source'])

        layer = data_source[0]

        print(' ' + str(layer.fields))

        for feature in layer:
            name = str(feature['COUNTRY'])

            country = None

            for item in Country.objects.filter(name=name):
                country = item

            if country is None:
                country = Country(name=name)

            print('Importing ' + name + '...')

            wkt = feature.geom.wkt

            if wkt.startswith('POLYGON (('):
                wkt = wkt.replace('POLYGON ((', 'MULTIPOLYGON (((')
                wkt = wkt + ')'

            country.bounds = GEOSGeometry(wkt)

            country.center = country.bounds.centroid

            country.save()
