from __future__ import print_function
from builtins import str
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from atlas.models import PhoneAreaCode

class Command(BaseCommand):
    help = 'Imports boundaries from shapefile files.'

    def add_arguments(self, parser):
        parser.add_argument('shapefile', nargs=1, type=str)

    def handle(self, *args, **options):
        shp_file = options['shapefile'][0]

        data_source = DataSource(shp_file)

        layer = data_source[0]

        print(' ' + str(layer.fields))

        for feature in layer:
            name = str(feature['NPA'])

            area_code = None

            for item in PhoneAreaCode.objects.filter(name=name):
                area_code = item

            if area_code is None:
                area_code = PhoneAreaCode(name=name)

            print('Importing ' + name + '...')

            wkt = feature.geom.wkt

            if wkt.startswith('POLYGON (('):
                wkt = wkt.replace('POLYGON ((', 'MULTIPOLYGON (((')
                wkt = wkt + ')'

            area_code.bounds = GEOSGeometry(wkt)

            area_code.center = area_code.bounds.centroid

            area_code.save()
