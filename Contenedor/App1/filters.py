# En un archivo filters.py dentro de tu aplicación

import django_filters
from .models import Alumno

class AlumnoFilter(django_filters.FilterSet):
    escuela_profesional = django_filters.CharFilter(field_name='Escuela_profesional__nombre', lookup_expr='icontains')

    class Meta:
        model = Alumno
        fields = ['escuela_profesional']
