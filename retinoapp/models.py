from django.db import models

# Create your models here. esto es para crear los modelos de la base de datos
#Tabla para los datos del paciente
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    email = models.EmailField(unique=True, null=True, blank=True)  # Opcional si quieres

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
#Tabla para las imagenes de retina
class ImagenRetina(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='retinas/')
    resultado = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente.nombre} - {self.fecha.date()}"
