from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from coreapp.models import Report
from coreapp.forms import ReportForm
from coreapp.graph_utils import plot_trend, plot_regions
import pandas as pd
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os



def home(request): 
    trends_html = plot_trend()
    table_html = plot_regions()

    context = {'trends_html': trends_html, 'table_html': table_html, }
    return render(request, "coreapp/index.html", context)   

# def index(request):
#     return render(request, "coreapp/index.html") 

def control_mitigation(request):
    return render(request, "coreapp/mitigation.html")

def self_report(request):
    return render(request, "coreapp/self_report.html")

def dashboard(request):
    
    trends_html = plot_trend()
    table_html = plot_regions()

    context = {'trends_html': trends_html, 'table_html': table_html, }
    
    return render(request, "coreapp/dashboard.html", context)



# Check the File Path
def download_data(request):
    file_path = os.path.join(settings.BASE_DIR, "Datasets/data.csv")

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file)
            return response
    else:
        raise Http404("File not found")
    


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
    

