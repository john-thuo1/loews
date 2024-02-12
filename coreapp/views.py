from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from coreapp.models import Report
from coreapp.forms import ReportForm


from coreapp.graph_utils import plot_trend, plot_regions
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
import os
from django.http import JsonResponse
from openai import OpenAI

from django.contrib import auth
from django.contrib.auth.models import User
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
    

