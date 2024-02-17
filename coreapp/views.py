from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from coreapp.models import Report
from coreapp.forms import ReportForm
from django.http import HttpResponse

import csv

from coreapp.graph_utils import plot_trend, plot_regions, plot_seasonality
import os
from django.http import JsonResponse
from openai import OpenAI

from .models import Chat

from django.utils import timezone
from decouple import config
import re

client = OpenAI(
    api_key=config("OPENAI_API_KEY"),
)


def home(request): 
    trends_html = plot_trend()

    context = {"trends_html": trends_html}
    return render(request, "coreapp/index.html", context)   



def control_mitigation(request):
    return render(request, "coreapp/mitigation.html")

def self_report(request):
    return render(request, "coreapp/self_report.html")

def dashboard(request):
    
    trends_html = plot_trend()
    table_html = plot_regions()[0]
    season_html = plot_seasonality()

    context = {'trends_html': trends_html, 'table_html': table_html, 'season_html':season_html}
    
    return render(request, "coreapp/dashboard.html", context)



def download_data(request):
    # Fetch data from the Report model
    reports_data = Report.objects.all().values()

    columns_to_drop = ['name', 'phone_number']

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cleaned_data.csv"'

    # Create a CSV writer
    csv_writer = csv.writer(response)

    # Write the header row excluding specified columns
    header_row = [field for field in reports_data[0] if field not in columns_to_drop]
    csv_writer.writerow(header_row)

    # Write the data rows excluding specified columns
    for report in reports_data:
        cleaned_report = [report[field] for field in header_row]
        csv_writer.writerow(cleaned_report)

    return response
    

 

def query_chat(message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a locust outbreak mitigation expert."},
            {"role": "user", "content": message},
            
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer


def format_response(response):
    lines = response.split('\n')
    formatted_lines = []

    for line in lines:
        if line.strip():
            # Check if the line starts with a number or bullet point
            is_numbered = re.match(r'^\s*\d+\.\s+', line)
            is_bulleted = re.match(r'^\s*-\s+', line)

            if is_numbered:
                formatted_lines.append(f'<p>{line.strip()}</p>')
            elif is_bulleted:
                formatted_lines.append(f'<p>{line.strip()}</p>')
            else:
                # Default to numbered list if the format is not detected
                formatted_lines.append(f'<p>{line.strip()}</p>')

    return ''.join(formatted_lines)

def rag_chat(request):
    
        # Ensure that the user is authenticated
    
    chats = Chat.objects.filter(user=request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        response = query_chat(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({"message": message, "response": format_response(response)})
    
    return render(request, "coreapp/chat.html", {"chats": chats})
    
def delete_chats(request):
    if request.method == "DELETE":
        Chat.objects.filter(user=request.user).delete()
        return JsonResponse({"message": "Chats deleted successfully"})
    else:
        return JsonResponse({"error": "Invalid method. Use DELETE."})
        

def contact_message(request):
    return render(request, "coreapp/contact.html")



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
    


