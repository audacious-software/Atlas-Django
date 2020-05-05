from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from atlas.models import TimeZone

class Command(BaseCommand):
    help = 'Imports boundaries from shapefile files.'

    def handle(self, *args, **options):
        shp_file = args[0]

        data_source = DataSource(shp_file)

        layer = data_source[0]

        print ' ' + str(layer.fields)

        for feature in layer:
            name = str(feature['TZID'])
            print 'Importing ' + name + '...'

            timezone = TimeZone(name=name)

            wkt = feature.geom.wkt

            if wkt.startswith('POLYGON (('):
                wkt = wkt.replace('POLYGON ((', 'MULTIPOLYGON (((')
                wkt = wkt + ')'

            timezone.bounds = GEOSGeometry(wkt)

            timezone.save()
