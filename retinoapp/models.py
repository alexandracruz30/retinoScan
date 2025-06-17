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
    GRADOS_RD = [
        ('0', 'Sin Retinopatía'),
        ('1', 'RD Leve'),
        ('2', 'RD Moderada'),
        ('3', 'RD Severa'),
        ('4', 'RD Proliferativa'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='retinas/')
    nombre_escaneo = models.CharField(max_length=200, default="Escaneo")
    resultado = models.CharField(max_length=2, choices=GRADOS_RD)
    confianza = models.FloatField(default=0.0)  # Porcentaje de confianza del modelo
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.paciente.nombre} - {self.nombre_escaneo} - {self.fecha.date()}"
    
    def get_severity_class(self):
        """Retorna clase CSS según la severidad"""
        severity_map = {
            '0': 'normal',
            '1': 'mild',
            '2': 'moderate', 
            '3': 'severe',
            '4': 'proliferative'
        }
        return severity_map.get(self.resultado, 'normal')
    
    def get_severity_description(self):
        """Retorna descripción detallada"""
        descriptions = {
            '0': 'No se detectaron signos de retinopatía diabética.',
            '1': 'Presencia de microaneurismas únicamente.',
            '2': 'Hemorragias y/o microaneurismas, con o sin exudados duros.',
            '3': 'Hemorragias abundantes y microaneurismas en 4 cuadrantes.',
            '4': 'Presencia de neovascularización y/o hemorragias vítreas.'
        }
        return descriptions.get(self.resultado, '')

    class Meta:
        ordering = ['-fecha']