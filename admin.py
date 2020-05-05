from django.contrib.gis import admin

from atlas.models import PostalCode, Province, TimeZone, PhoneAreaCode

class PostalCodeAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'country', 'center')
    list_filter = ['country']

    search_fields = ['name', 'country']

admin.site.register(PostalCode, PostalCodeAdmin)

class ProvinceAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'abbreviation', 'country', 'center')
    list_filter = ['country']

    search_fields = ['name', 'country', 'abbreviation']

admin.site.register(Province, ProvinceAdmin)

class TimeZoneAdmin(admin.OSMGeoAdmin):
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(TimeZone, TimeZoneAdmin)

class PhoneAreaCodeAdmin(admin.OSMGeoAdmin):
    list_display = ('name',)
    search_fields = ['name']

admin.site.register(PhoneAreaCode, PhoneAreaCodeAdmin)
