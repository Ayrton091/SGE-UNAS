from django.shortcuts import render
import matplotlib
matplotlib.use('agg')
from django.views.generic import ListView
from django.shortcuts import render
from .models import Escuela_profesional, Alumno
import matplotlib.pyplot as plt
from .filters import AlumnoFilter


# Create your views here.


def IndexView (request):
    '''Esto es la pagina principal'''
    return render(request,"index.html")



def grafico_alumnos_por_escuela(request):
    # Realizar la consulta para obtener la cantidad de alumnos por escuela profesional
    escuelas = Escuela_profesional.objects.all()
    datos_escuelas = []
    for escuela in escuelas:
        cantidad_alumnos = Alumno.objects.filter(Escuela_profesional=escuela).count()
        datos_escuelas.append((escuela.nombre, cantidad_alumnos))

    # Preparar los datos para graficar
    nombres_escuelas = [escuela[0] for escuela in datos_escuelas]
    cantidad_alumnos = [escuela[1] for escuela in datos_escuelas]

    # Graficar los datos
    plt.bar(nombres_escuelas, cantidad_alumnos)
    plt.xlabel('Escuela Profesional')
    plt.ylabel('Cantidad de Alumnos')
    plt.title('Cantidad de Alumnos por Escuela Profesional')
    plt.xticks(rotation=45)  # Rotar los nombres de las escuelas para mejor visualización
    plt.tight_layout()

    # Guardar la imagen del gráfico (opcional)
    # plt.savefig('alumnos_por_escuela.png')

    # Convertir el gráfico a formato base64 para incrustarlo en la plantilla HTML
    import io
    import base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render(request, 'grafico.html', {'grafico_base64': grafico_base64})

class AlumnoListView(ListView):
    model = Alumno
    template_name = 'alumno_list.html'
    context_object_name = 'alumnos'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filters = AlumnoFilter(self.request.GET, queryset=queryset)
        return self.filters.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filters
        return context
    
#def alumno(request):
 #   return render(request,'alumno_list.html')