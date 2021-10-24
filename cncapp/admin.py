from django.contrib import admin
from . import models

# admin.site.register(models.CncProg)
admin.site.register(models.Profile)
admin.site.register(models.MyCutter)
# admin.site.register(models.Information)
admin.site.register(models.Comment)
# admin.site.register(models.InformationCategory)


@admin.register(models.CncProg)
class CncProgAdmin(admin.ModelAdmin):
    list_display = ('material', 'teeth_numbers', 'cutter_diameter', 'spindel_speed_min', 'spindel_speed_max',
                    'moving_speed_min', 'moving_speed_max')


@admin.register(models.Information)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'category')
    list_filter = ('category', )
    search_fields = ('title', )
    prepopulated_fields = {'slug': ('title', )}


@admin.register(models.InformationCategory)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}