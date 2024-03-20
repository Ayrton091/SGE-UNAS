
from django.contrib import admin
from django.urls import path
from App1.views import IndexView , grafico_alumnos_por_escuela, AlumnoListView
#from App1.views import alumno

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",IndexView),
    path('graficos/', grafico_alumnos_por_escuela, name='graficos'), # Asigna una URL a tu vista
    path('alumnos/', AlumnoListView.as_view(), name='alumno_list'),    
    
]
