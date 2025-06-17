from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Paciente, ImagenRetina
import random  # Simular modelo IA, reemplaza con tu modelo real
from django.contrib.auth.decorators import login_required

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

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

def home_view(request):
    return render(request, 'home.html')

@login_required
def patient_register_view(request):
    if request.method == 'POST':
        paciente = Paciente(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            cedula=request.POST.get('cedula'),
            fecha_nacimiento=request.POST.get('fecha_nacimiento'),
            grupo_sanguineo=request.POST.get('grupo_sanguineo'),
            alergias=request.POST.get('alergias'),
            enfermedades_cronicas=request.POST.get('enfermedades'),
        )
        
        if 'foto' in request.FILES:
            paciente.foto = request.FILES['foto']
            
        paciente.save()
        return redirect('patient_detail', paciente_id=paciente.id)
        
    return render(request, 'patient_register.html')

@login_required
def patient_history_view(request):
    patients = Paciente.objects.all()
    print(f"Número de pacientes encontrados: {patients.count()}")  # Debug
    return render(request, 'patient_history.html', {'patients': patients})

def patient_detail_view(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    detections = paciente.imagenes.order_by('-fecha')
    return render(request, 'patient_detail.html', {
        'patient': paciente,
        'detections': detections
    })

def upload_image_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        if 'imagen' in request.FILES:
            imagen_file = request.FILES['imagen']
            nombre_escaneo = request.POST.get('nombre_escaneo', 'Escaneo')
            
            # Guardar la imagen en la carpeta retinas
            import os
            import uuid
            from django.core.files.storage import default_storage
            
            # Generar nombre único para la imagen
            file_extension = os.path.splitext(imagen_file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Guardar en la carpeta retinas
            file_path = os.path.join('/Users/alexandracruz/Documents/Proyectos/retinoScan/retinas', unique_filename)
            
            with open(file_path, 'wb+') as destination:
                for chunk in imagen_file.chunks():
                    destination.write(chunk)
            
            # Simular análisis de IA
            resultado = "Retinopatía diabética leve detectada"
            
            # Crear registro en la base de datos
            detection = ImagenRetina.objects.create(
                paciente=paciente,
                imagen=unique_filename,  # Solo el nombre del archivo
                resultado=resultado,
                nombre_escaneo=nombre_escaneo
            )
            
            return redirect('result_view', detection_id=detection.id)
        
    return render(request, 'upload_image.html', {'patient': paciente})

def simular_diagnostico_ia(imagen):
    """
    REEMPLAZA ESTA FUNCIÓN CON TU MODELO REAL DE DEEP LEARNING
    """
    # Simulación temporal
    grados = ['0', '1', '2', '3', '4']
    return {
        'grado': random.choice(grados),
        'confianza': round(random.uniform(75.0, 99.5), 1)
    }

def result_view(request, detection_id):
    detection = get_object_or_404(ImagenRetina, id=detection_id)
    return render(request, 'result.html', {'detection': detection})

def delete_detection_view(request, detection_id):
    detection = get_object_or_404(ImagenRetina, id=detection_id)
    paciente_id = detection.paciente.id
    
    if request.method == 'POST':
        detection.delete()
        messages.success(request, 'Registro eliminado correctamente')
        return redirect('patient_detail', paciente_id=paciente_id)
    
    return render(request, 'confirm_delete.html', {'detection': detection})

@login_required
def patient_edit_view(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        paciente.nombre = request.POST.get('nombre')
        paciente.apellido = request.POST.get('apellido')
        paciente.cedula = request.POST.get('cedula')
        paciente.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        paciente.grupo_sanguineo = request.POST.get('grupo_sanguineo')
        paciente.alergias = request.POST.get('alergias')
        paciente.enfermedades_cronicas = request.POST.get('enfermedades')
        
        if 'foto' in request.FILES:
            paciente.foto = request.FILES['foto']
            
        paciente.save()
        return redirect('patient_detail', paciente_id=paciente.id)
        
    return render(request, 'patient_edit.html', {'paciente': paciente})