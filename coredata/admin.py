# Register your models here.
from django.contrib import admin

# Register your models here.
# from core.refs.models import Country, Region
from coredata.models import District, Region, Reference, User, SamplesSniffer
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from leaflet.admin import LeafletGeoAdmin


class UsersAdmin(DjangoUserAdmin):
    list_display = ('pk', 'email')
    model = User
    fieldsets = DjangoUserAdmin.fieldsets + (
        (None, {
            'fields': ('user_role', 'district', 'region',),
        }),
    )


admin.site.register(User, UsersAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_local')


admin.site.register(District, DistrictAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_uz', 'coefficient')


admin.site.register(Region, RegionAdmin)


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_uz', 'type',)
    ordering = ('-added_at',)


admin.site.register(Reference, LeafletGeoAdmin)


class SamplesSnifferAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_uz', 'limit', 'added_at')
    ordering = ('-added_at',)


admin.site.register(SamplesSniffer, SamplesSnifferAdmin)
