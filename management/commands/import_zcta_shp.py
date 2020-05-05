from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from atlas.models import PostalCode

class Command(BaseCommand):
    help = 'Imports boundaries from shapefile files.'

    def add_arguments(self, parser):
        parser.add_argument('zipcode_file')

    def handle(self, *args, **options):
        shp_file = options['zipcode_file']

        data_source = DataSource(shp_file)

        layer = data_source[0]

        print ' ' + str(layer.fields)

        for feature in layer:
            zcta = str(feature['ZCTA5CE10'])

            postal_code = None

            for code in PostalCode.objects.filter(name=zcta, country='us'):
                postal_code = code

            if postal_code is None:
                postal_code = PostalCode(name=zcta, country='us')

            print 'Importing ' + zcta + '...'

            wkt = feature.geom.wkt

            if wkt.startswith('POLYGON (('):
                wkt = wkt.replace('POLYGON ((', 'MULTIPOLYGON (((')
                wkt = wkt + ')'

            postal_code.bounds = GEOSGeometry(wkt)
            postal_code.center = postal_code.bounds.centroid

            postal_code.save()
