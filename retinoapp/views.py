from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Django usa username por defecto, necesitas buscar el usuario por email
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'login.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def home_view(request):
    return render(request, 'home.html')