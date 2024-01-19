from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'phone_number', 'report_date', 'species', 'stage', 'size', 'distribution', 
                  'image', 'location','season','vegetation_details', 'gps_coordinates']
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
        }
