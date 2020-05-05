from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from atlas.models import Province

class Command(BaseCommand):
    help = 'Imports boundaries from shapefile files.'

    def handle(self, *args, **options):
        shp_file = args[0]

        data_source = DataSource(shp_file)

        layer = data_source[0]

        print ' ' + str(layer.fields)

        for feature in layer:
            name = str(feature['NAME'])
            abbreviation = str(feature['STUSPS'])

            province = None

            for item in Province.objects.filter(name=name, country='us'):
                province = item

            if province is None:
                province = Province(name=name, abbreviation=abbreviation, country='us')

            print 'Importing ' + name + '...'

            wkt = feature.geom.wkt

            if wkt.startswith('POLYGON (('):
                wkt = wkt.replace('POLYGON ((', 'MULTIPOLYGON (((')
                wkt = wkt + ')'

            province.bounds = GEOSGeometry(wkt)
            pnt_wkt = 'POINT(' +  str(feature['INTPTLON']).replace('+', '') + ' ' + \
                      str(feature['INTPTLAT']).replace('+', '') + ')'

            province.center = GEOSGeometry(pnt_wkt)

            province.save()
