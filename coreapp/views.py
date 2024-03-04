# Standard Library Imports
import csv
import re


# Third-party Library Imports
from bs4 import BeautifulSoup
from decouple import config
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from PyPDF2 import PdfReader


# Local Imports
from .forms import ReportForm
from .graph_utils import (plot_trend, plot_regions, plot_seasonality, plot_vegetation)
from .models import Report
from openai import OpenAI
from .models import Chat


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
    vegetation_html = plot_vegetation()
    context = {'trends_html': trends_html, 'table_html': table_html, 
               'season_html': season_html, 'vegetation_html': vegetation_html}
    
    return render(request, "coreapp/dashboard.html", context)
 
 


 
def load_data():
    pdf = "..\loews\Datasets\pesticides.pdf"
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
        

def process_text(text):
    text_splitter = CharacterTextSplitter(separator="\n", keep_separator=True, chunk_size=1000, 
                                          chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(text)
    
    embeddings = OpenAIEmbeddings(api_key=config("OPENAI_API_KEY"))
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    return knowledgeBase


def query_chat(message, similar_documents):
    similar_documents = [str(doc_id) for doc_id in similar_documents]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a locust outbreak mitigation expert."},
            {"role": "user", "content": message},
            {"role": "system", "content": "Similar documents: \n" + "\n".join(similar_documents)}
       
        ]
    )
    answer = response.choices[0].message.content.strip()
    return answer


# Format response prior to saving to db
def format_response(response):
    lines = response.split('\n')
    formatted_lines = []
    for line in lines:
        if line.strip():
            is_numbered = re.match(r'^\s*\d+\.\s+', line)
            is_bulleted = re.match(r'^\s*-\s+', line)

            if is_numbered:
                formatted_lines.append(f'<p>{line.strip()}</p>')
            elif is_bulleted:
                formatted_lines.append(f'<p>{line.strip()}</p>')
            else:
                formatted_lines.append(f'<p>{line.strip()}</p>')
    return ''.join(formatted_lines)


def rag_chat(request): 
    chats = Chat.objects.filter(user=request.user)
    if request.method == "POST":
        # User Query
        message = request.POST.get("message")
        
        document = load_data()
        knowledge_base = process_text(document)
        similar_documents = knowledge_base.similarity_search(message)
        
        response = query_chat(message, similar_documents)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({"message": message, "response": format_response(response)})
    return render(request, "coreapp/chat.html", {"chats": chats})


def download_data(request):
    reports_data = Report.objects.all().values()
    columns_to_drop = ['name', 'phone_number']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="locusts_data.csv"'
    csv_writer = csv.writer(response)
    header_row = [field for field in reports_data[0] if field not in columns_to_drop]
    csv_writer.writerow(header_row)

    # Write the data rows excluding specified columns
    for report in reports_data:
        cleaned_report = [report[field] for field in header_row]
        csv_writer.writerow(cleaned_report)
    return response

    
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



