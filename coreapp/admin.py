from django.contrib import admin
from .models import Report, Chat
from import_export.admin import ImportExportMixin


class ReportAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'report_date', 'species', 'stage', 'size', 'distribution', 
                    'image','location','season','soil_type','vegetation_details')
    

admin.site.register(Report, ReportAdmin)
admin.site.register(Chat)

