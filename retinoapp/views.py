from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'login.html')    

def dashboard_view(request):
    return render(request, 'dashboard.html')

def home_view(request):
    return render(request, 'home.html')