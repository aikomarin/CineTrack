import requests
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SeriePeliculaForm
from rest_framework import viewsets
from .models import SeriePelicula
from .serializers import SeriePeliculaSerializer
from .utils import buscar_contenido_tmdb
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.html import escape


def home(request):
    contenidos_con_imagen = SeriePelicula.objects.exclude(imagen__isnull=True).exclude(imagen__exact='').order_by('?')[:15]
    pendientes = SeriePelicula.objects.filter(estado='pendiente')[:11]

    return render(request, 'home.html', {
        'contenido_con_imagen': contenidos_con_imagen,
        'pendientes': pendientes
    })


def registrar_contenido(request):
    mensaje_error = None

    if request.method == 'POST':
        form = SeriePeliculaForm(request.POST)

        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            plataforma = form.cleaned_data['plataforma']

            if SeriePelicula.objects.filter(titulo=titulo, plataforma=plataforma).exists():
                mensaje_error = "Este contenido ya fue registrado previamente."
            else:
                form.save()
                return redirect('listar_contenido')
    else:
        form = SeriePeliculaForm()

    return render(request, 'registrar.html', {'form': form, 'mensaje_error': mensaje_error})


def listar_contenido(request):
    contenidos = SeriePelicula.objects.all()

    tipo = request.GET.get('tipo')
    plataforma = request.GET.get('plataforma')
    estado = request.GET.get('estado')

    if tipo:
        contenidos = contenidos.filter(tipo=tipo)
    if plataforma:
        contenidos = contenidos.filter(plataforma=plataforma)
    if estado:
        contenidos = contenidos.filter(estado=estado)

    # Mostrar todas las plataformas posibles
    plataformas_disponibles = sorted(SeriePelicula.PLATAFORMAS, key=lambda x: x[1])

    # Ordenar alfabéticamente por título por defecto
    contenidos = contenidos.order_by('titulo')

    return render(request, 'lista.html', {
        'contenidos': contenidos,
        'plataformas': plataformas_disponibles,
        'filtros': {
            'tipo': tipo,
            'plataforma': plataforma,
            'estado': estado,
        },
    })


def editar_contenido(request, pk):
    contenido = get_object_or_404(SeriePelicula, pk=pk)

    if request.method == 'POST':
        print("🔧 Se recibió POST")  # <-- agrega esto
        form = SeriePeliculaForm(request.POST, instance=contenido)
        if form.is_valid():
            print("✅ Formulario válido")  # <-- agrega esto
            form.save()
            return redirect('listar_contenido')
        else:
            print("❌ Formulario inválido:", form.errors)  # <-- y esto
    else:
        form = SeriePeliculaForm(instance=contenido)

    return render(request, 'editar.html', {
        'form': form,
        'contenido': contenido
    })


def eliminar_contenido(request, pk):
    contenido = get_object_or_404(SeriePelicula, pk=pk)
    if request.method == 'POST':
        contenido.delete()
        return redirect('listar_contenido')
    return render(request, 'eliminar.html', {'contenido': contenido})


class SeriePeliculaViewSet(viewsets.ModelViewSet):
    queryset = SeriePelicula.objects.all()
    serializer_class = SeriePeliculaSerializer


def buscar_contenido(request):
    resultados = []
    if request.method == "POST":
        query = request.POST.get("query")
        resultados = buscar_contenido_tmdb(query)

    # ordenar alfabéticamente por etiqueta, dejando 'otro' al final
    opciones = list(SeriePelicula.PLATAFORMAS)  # [('netflix','Netflix'), ... , ('otro','Otra')]
    otras = [x for x in opciones if x[0] == 'otro']
    normales = sorted([x for x in opciones if x[0] != 'otro'], key=lambda x: x[1].lower())
    plataformas_ordenadas = normales + otras

    return render(request, "buscar.html", {
        "resultados": resultados,
        "plataformas": plataformas_ordenadas,
    })


@csrf_exempt
def guardar_desde_busqueda(request):
    if request.method == 'POST':
        # Este es el título que TÚ escribiste manualmente (viene desde un input hidden)
        titulo_usuario = request.POST.get('titulo_usuario')
        plataforma = request.POST.get('plataforma')

        if SeriePelicula.objects.filter(titulo=titulo_usuario, plataforma=plataforma).exists():
            messages.warning(request, f"⚠️ '{escape(titulo_usuario)}' ya existe en tu lista.")
            return redirect('buscar_contenido')

        SeriePelicula.objects.create(
            titulo=titulo_usuario,
            resumen=request.POST.get('resumen'),
            fecha=request.POST.get('fecha') or None,
            imagen=request.POST.get('imagen'),
            tipo=request.POST.get('tipo'),
            plataforma=plataforma,
            calificacion=request.POST.get('calificacion') or None,
            veces_vista=request.POST.get('veces_vista') or 0,
            volveria_a_ver=bool(request.POST.get('volveria_a_ver')),
            estado=request.POST.get('estado'),
            tendra_continuacion=request.POST.get('tendra_continuacion') == 'on',
            favorita=request.POST.get('favorita') == 'on',
        )
        messages.success(request, f"✅ '{escape(titulo_usuario)}' fue registrada exitosamente.")
        return redirect('buscar_contenido')

    return redirect('buscar_contenido')


def detalle_contenido(request, pk):
    contenido = get_object_or_404(SeriePelicula, pk=pk)
    return render(request, 'detalle_contenido.html', {'contenido': contenido})


def pendientes(request):
    peliculas = (SeriePelicula.objects
                 .filter(estado='pendiente', tipo='pelicula')
                 .order_by('titulo'))
    series = (SeriePelicula.objects
              .filter(estado='pendiente', tipo='serie')
              .order_by('titulo'))

    return render(request, "pendientes.html", {
        "peliculas": peliculas,
        "series": series,
        "count_peliculas": peliculas.count(),
        "count_series": series.count(),
    })


def marcar_vista(request, pk):
    # acción rápida para cambiar de pendiente -> vista
    if request.method == "POST":
        item = get_object_or_404(SeriePelicula, pk=pk)
        item.estado = "vista"
        # opcional: sumar una vez vista si quieres
        # item.veces_vista = (item.veces_vista or 0) + 1
        item.save(update_fields=["estado"])  # o ["estado","veces_vista"]
    return redirect("pendientes")


def favoritas(request):
    peliculas = (SeriePelicula.objects
                 .filter(favorita=True, tipo='pelicula')
                 .order_by('titulo'))
    series = (SeriePelicula.objects
              .filter(favorita=True, tipo='serie')
              .order_by('titulo'))

    return render(request, "favoritas.html", {
        "peliculas": peliculas,
        "series": series,
        "count_peliculas": peliculas.count(),
        "count_series": series.count(),
    })


def toggle_favorita(request, pk):
    if request.method == "POST":
        item = get_object_or_404(SeriePelicula, pk=pk)
        # Alternar: si es True -> False, si es False/None -> True
        item.favorita = not bool(item.favorita)
        item.save(update_fields=["favorita"])
    return redirect("favoritas")

