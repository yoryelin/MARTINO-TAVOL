from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('maquina/<int:pk>/', views.detalle_maquina, name='detalle_maquina'),
    path('enviar-consulta/', views.enviar_consulta, name='enviar_consulta'),
    path('activar-radar-maquinaria/', views.activar_radar_maquinaria, name='activar_radar'),
]
