from django.db import models

# Create your models here. esto es para crear los modelos de la base de datos
#Tabla para los datos del paciente
class Paciente(models.Model):
    # Datos Personales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    foto = models.ImageField(upload_to='pacientes/', null=True, blank=True)
    
    # Datos Médicos Iniciales
    GRUPOS_SANGUINEOS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    grupo_sanguineo = models.CharField(
        max_length=3,
        choices=GRUPOS_SANGUINEOS,
        null=True,
        blank=True
    )
    alergias = models.TextField(null=True, blank=True)
    enfermedades_cronicas = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
#Tabla para las imagenes de retina
class ImagenRetina(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='retinas/')
    resultado = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente.nombre} - {self.fecha.date()}"
