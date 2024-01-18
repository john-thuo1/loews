from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'description', 'report_date']
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
        }
