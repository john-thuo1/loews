# Standard Library Imports
import csv
import re
import os

# Third-party Library Imports
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from dotenv import load_dotenv
from django.views.generic import CreateView
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pypdf import PdfReader
from coreapp.logger import setup_logger

# Local Imports
from .forms import ReportForm
from .graph_utils import (plot_trend, plot_regions, plot_seasonality, plot_vegetation, plot_predictionmap)
from .models import Report, Chat
from openai import OpenAI


load_dotenv() 

user_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=user_api_key)

logger = setup_logger(__name__, 'views.log')


def control_mitigation(request):
    try:
        logger.info("Accessing mitigation control")
        return render(request, "coreapp/mitigation.html")
    except Exception as e:
        logger.error(f"Error in control_mitigation: {e}")
        return HttpResponseServerError("An error occurred while accessing mitigation control.")


def self_report(request):
    try:
        logger.info("Accessing self report")
        return render(request, "coreapp/self_report.html")
    except Exception as e:
        logger.error(f"Error in self_report: {e}")
        return HttpResponseServerError("An error occurred while accessing self report.")


def dashboard(request):
    try:
        logger.info("Accessing dashboard")
        trends_html = plot_trend()
        table_html = plot_regions()[0]
        season_html = plot_seasonality()
        vegetation_html = plot_vegetation()
        context = {'trends_html': trends_html, 'table_html': table_html, 
                   'season_html': season_html, 'vegetation_html': vegetation_html}
        return render(request, "coreapp/dashboard.html", context)
    except Exception as e:
        logger.error(f"Error in dashboard: {e}")
        return HttpResponseServerError("An error occurred while accessing dashboard.")


def load_data():
    try:
        logger.info("Loading data")
        pdf_path = "Datasets/pesticides.pdf"
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file '{pdf_path}' not found.")
            return ""
        
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        logger.error(f"Error in load_data: {e}")
        return ""


def process_text(text):
    try:
        logger.info("Processing text")
        text_splitter = CharacterTextSplitter(separator="\n", keep_separator=True, chunk_size=1000, 
                                              chunk_overlap=200, length_function=len)
        chunks = text_splitter.split_text(text)
        
        embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
        knowledgeBase = FAISS.from_texts(chunks, embeddings)
        return knowledgeBase
    except Exception as e:
        logger.error(f"Error in process_text: {e}")
        return None


def query_chat(message, similar_documents):
    try:
        logger.info("Querying chat")
        similar_documents = [str(doc_id) for doc_id in similar_documents]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a locust outbreak mitigation expert. If you do not know the answer, or are unsure, say you don't know."},
                {"role": "user", "content": message},
                {"role": "system", "content": "Similar documents: \n" + "\n".join(similar_documents)}
            
            ]
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        logger.error(f"Error in query_chat: {e}")
        return "Sorry, an error occurred while processing your request."


def format_response(response):
    try:
        logger.info("Formatting response")
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
    except Exception as e:
        logger.error(f"Error in format_response: {e}")
        return "Sorry, an error occurred while processing your request."


def rag_chat(request): 
    try:
        logger.info("Chatting")
        chats = Chat.objects.filter(user=request.user)
        if request.method == "POST":
            # User Query
            message = request.POST.get("message")
            
            document_text = load_data()
            knowledge_base = process_text(document_text)
            if knowledge_base:
                similar_documents = knowledge_base.similarity_search(message)
                response = query_chat(message, similar_documents)
                chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
                chat.save()
                return JsonResponse({"message": message, "response": format_response(response)})
            else:
                return JsonResponse({"error": "An error occurred while processing the document."})
        return render(request, "coreapp/chat.html", {"chats": chats})
    except Exception as e:
        logger.error(f"Error in rag_chat: {e}")
        return HttpResponseServerError("An error occurred while accessing the chat.")


def download_data(request):
    try:
        logger.info("Downloading data")
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
    except Exception as e:
        logger.error(f"Error in download_data: {e}")
        return HttpResponseServerError("An error occurred while downloading data.")


def delete_chats(request):
    try:
        logger.info("Deleting chats")
        if request.method == "DELETE":
            Chat.objects.filter(user=request.user).delete()
            return JsonResponse({"message": "Chats deleted successfully"})
        else:
            return JsonResponse({"error": "Invalid method. Use DELETE."})
    except Exception as e:
        logger.error(f"Error in delete_chats {e}")

       

def map_predictions(request):
    try:
        logger.info("Generating prediction map")
        map_html = plot_predictionmap()
        context = {'map_html': map_html._repr_html_()}
        return render(request, "coreapp/index.html", context)
    except Exception as e:
        logger.error(f"Error in map_predictions: {e}")
        return HttpResponseServerError("An error occurred while generating prediction map.")


def dashboard(request):
    try:
        logger.info("Generating dashboard")
        trends_html = plot_trend()
        table_html = plot_regions()[0]
        season_html = plot_seasonality()
        vegetation_html = plot_vegetation()
        context = {'trends_html': trends_html, 'table_html': table_html, 
                   'season_html': season_html, 'vegetation_html': vegetation_html}
        return render(request, "coreapp/dashboard.html", context)
    except Exception as e:
        logger.error(f"Error in dashboard: {e}")
        return HttpResponseServerError("An error occurred while generating dashboard.")


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



