from coreapp.views import *
from django.urls import path

urlpatterns = [
    path("chat/", rag_chat, name="rag-chat"),
    path("mitigating-controls/", control_mitigation, name="mitigation"),
    path("self-reporting/", SelfReportCreateView.as_view(), name="report"),
    path("dashboard/", dashboard, name="dashboard"),
    path('download/', download_data, name="download_data"),
    path("delete-chats/", delete_chats, name="delete_chats"),
    path("", map_predictions, name="map_predictions")
    
]