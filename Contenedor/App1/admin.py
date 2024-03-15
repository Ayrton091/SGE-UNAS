from django.contrib import admin
from django.contrib import admin
from .models import Alumno, Egresado, Escuela_profesional, Trayectoria

# Registra tus modelos aquí

admin.site.register(Alumno)
admin.site.register(Egresado)
admin.site.register(Escuela_profesional)
admin.site.register(Trayectoria)
