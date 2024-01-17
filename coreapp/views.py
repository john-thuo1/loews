from django.shortcuts import render


def home(request): 
    return render(request, 'coreapp/base.html')    

def control_mitigation(request):
    return render(request, "coreapp/mitigation.html")
