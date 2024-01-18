from django.contrib import admin
from .models import Report
from import_export.admin import ImportExportMixin


class ReportAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('name', 'description', 'report_date')
    

admin.site.register(Report, ReportAdmin)

