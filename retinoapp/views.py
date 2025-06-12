from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Paciente
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
#para registrar un usuario
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'El nombre de usuario ya existe'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'El correo ya está registrado'})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)  # Opcional: loguea automáticamente tras registro
        return redirect('dashboard')

    return render(request, 'register.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def home_view(request):
    return render(request, 'home.html')

def patient_register_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        paciente = Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            fecha_nacimiento=fecha_nacimiento
        )
        return redirect('patient_detail', patient_id=paciente.id)
    return render(request, 'patient_register.html')

def patient_history_view(request):
    return render(request, 'patient_history.html')