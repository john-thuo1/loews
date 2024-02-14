from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
        
        widgets = {
            'report_date': forms.DateInput(attrs={'type': 'date'}),
        }

