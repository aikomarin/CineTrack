# tracker/models.py

from django.db import models


class SeriePelicula(models.Model):
    PLATAFORMAS = [
        ('prime', 'Amazon Prime'),
        ('disney', 'Disney+'),
        ('hbo', 'HBO Max'),
        ('netflix', 'Netflix'),
        ('star', 'Star+'),
        ('vix', 'Vix'),
        ('otro', 'Otra'),
    ]

    ESTADOS = [
        ('vista', 'Vista'),
        ('pendiente', 'Pendiente'),
    ]

    CALIFICACIONES = [
        ('excelente', 'Excelente'),
        ('buena', 'Buena'),
        ('meh', 'Regular'),
        ('mala', 'Mala'),
        ('horrible', 'Horrible'),
    ]

    titulo = models.CharField(max_length=255)
    resumen = models.TextField(blank=True)
    fecha = models.DateField(null=True, blank=True)
    imagen = models.URLField(blank=True)
    tipo = models.CharField(max_length=10, choices=[('pelicula', 'Película'), ('serie', 'Serie')])
    plataforma = models.CharField(max_length=20, choices=PLATAFORMAS, blank=True)
    calificacion = models.CharField(max_length=10, choices=CALIFICACIONES, blank=True, null=True)
    veces_vista = models.IntegerField(default=0)
    volveria_a_ver = models.BooleanField(default=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    tendra_continuacion = models.BooleanField(default=False)
    favorita = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
