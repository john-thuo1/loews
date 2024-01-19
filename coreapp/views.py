from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from coreapp.models import Report
from coreapp.forms import ReportForm


def home(request): 
    return render(request, 'coreapp/base.html')    

def control_mitigation(request):
    return render(request, "coreapp/mitigation.html")

def self_report(request):
    return render(request, "coreapp/self_report.html")

class SelfReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'coreapp/self_report.html'

    def get_success_url(self):
        return reverse('report')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_title'] = 'Submit A Report on Locust Sightings'
        return context