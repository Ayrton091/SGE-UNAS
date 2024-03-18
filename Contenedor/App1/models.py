from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Escuela_profesional(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_creditos = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200)])

    def __str__(self):
        return f"{self.nombre} - {self.cantidad_creditos}"



class Alumno(models.Model):
    codigo_alumno = models.CharField(max_length=10, primary_key=True)
    dni = models.CharField(max_length=8)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    c_creditos = models.PositiveSmallIntegerField(validators=[MaxValueValidator(200)])
    Escuela_profesional = models.ForeignKey(Escuela_profesional, on_delete=models.CASCADE)
    numero_telefono = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.nombre} - {self.c_creditos} - {self.Escuela_profesional}"

class Egresado(models.Model):
    codigo_alumno = models.OneToOneField(Alumno, on_delete=models.CASCADE)
    fecha_egreso = models.DateField()
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.codigo_alumno.nombre




@receiver(post_save, sender=Alumno)
def verificar_egreso(sender, instance, created, **kwargs):
    if not created:  # Evitar ejecutar la lógica en la creación de un nuevo alumno
        escuela_profesional = instance.Escuela_profesional
        cantidad_creditos = escuela_profesional.cantidad_creditos
        creditos_alumno = instance.c_creditos
        if creditos_alumno >= cantidad_creditos:
            # Crear un registro en la tabla de egresados
            Egresado.objects.create(
                codigo_alumno=instance,
                fecha_egreso=instance.fecha_nacimiento,  # Ajusta esta fecha según sea necesario
                titulo="Título de egreso"  # Ajusta el título según sea necesario
            )



class Trayectoria(models.Model):
    egresado = models.ForeignKey(Egresado, on_delete=models.CASCADE, related_name='empleos')
    empresa = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)  # Puede ser null si el empleado todavía trabaja en esa empresa
    # Otros campos relacionados con el empleo

    def __str__(self):
        return f"{self.empresa} - {self.cargo} ({self.fecha_inicio} - {self.fecha_fin})"
