from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin
# Register your models here.
from samples.models import Sample,Oferta,type_service,inspection_general,product_type,Oferta_detail


class SamplesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'calculation_region', 'creator','area')


admin.site.register(Sample, LeafletGeoAdmin)
admin.site.register(Oferta)
admin.site.register(type_service)
admin.site.register(inspection_general)
admin.site.register(product_type)
admin.site.register(Oferta_detail)