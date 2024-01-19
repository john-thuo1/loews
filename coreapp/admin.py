from django.contrib import admin
from .models import Report
from import_export.admin import ImportExportMixin


class ReportAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'report_date', 'species', 'stage', 'size', 'distribution', 
                    'image','location','season','soil_type','vegetation_details', 'gps_coordinates')
    

admin.site.register(Report, ReportAdmin)

