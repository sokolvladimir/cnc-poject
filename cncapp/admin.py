from django.contrib import admin
from . import models

# admin.site.register(models.CncProg)
admin.site.register(models.Profile)
admin.site.register(models.MyCutter)


@admin.register(models.CncProg)
class CncProgAdmin(admin.ModelAdmin):
    list_display = ('material', 'teeth_numbers', 'cutter_diameter', 'spindel_speed_min', 'spindel_speed_max',
                    'moving_speed_min', 'moving_speed_max')
