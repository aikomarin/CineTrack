from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeriePeliculaViewSet
from . import views

router = DefaultRouter()
router.register(r'contenidos', SeriePeliculaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('buscar/', views.buscar_contenido, name='buscar_contenido'),
    path('guardar-desde-busqueda/', views.guardar_desde_busqueda, name='guardar_desde_busqueda'),
    path('contenido/<int:pk>/', views.detalle_contenido, name='detalle_contenido'),
    path('pendientes/', views.pendientes, name='pendientes'),
    path('pendientes/marcar-vista/<int:pk>/', views.marcar_vista, name='marcar_vista'),
    path('favoritas/', views.favoritas, name='favoritas'),
    path('favoritas/toggle/<int:pk>/', views.toggle_favorita, name='toggle_favorita'),
]
