# Create your views here.
# core/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Inmueble, Propietario, Inquilino, Contrato, Pago, Incidencia
from .forms import InmuebleForm, IncidenciaForm

@login_required
def home(request):
    return render(request, "home.html")

def user_in_group(user, name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name__iexact=name).exists()

@login_required
def dashboard(request):
    user = request.user
    if user.is_staff or user.is_superuser:
        return redirect("core:staff_panel")
    if user_in_group(user, "Propietarios"):
        return redirect("core:propietario_panel")
    if user_in_group(user, "Inquilinos"):
        return redirect("core:inquilino_panel")
    return render(request, "home.html")

@login_required
def propietario_panel(request):
    propietarios = Propietario.objects.filter(usuario=request.user).prefetch_related("inmuebles", "contratos")
    inmuebles = (
        Inmueble.objects.filter(propietario__usuario=request.user)
        .prefetch_related("incidencias", "pagos", "contratos")
    )
    contratos = (
        Contrato.objects.filter(propietario__usuario=request.user)
        .prefetch_related("inquilinos", "inmueble")
    )
    pagos = (
        Pago.objects.filter(inmueble__propietario__usuario=request.user)
        .select_related("tipo", "inmueble")
        .order_by("-fecha")[:20]
    )
    incidencias = (
        Incidencia.objects.filter(inmueble__propietario__usuario=request.user)
        .select_related("inmueble")
        .order_by("-fecha_reporte")[:20]
    )
    stats = {
        "inmuebles": inmuebles.count(),
        "contratos": contratos.count(),
        "pagos_pendientes": Pago.objects.filter(
            inmueble__propietario__usuario=request.user, pagado=False
        ).count(),
        "incidencias_abiertas": Incidencia.objects.filter(
            inmueble__propietario__usuario=request.user, fecha_resolucion__isnull=True
        ).count(),
    }
    return render(
        request,
        "core/panel_propietario.html",
        {
            "propietarios": propietarios,
            "inmuebles": inmuebles,
            "contratos": contratos,
            "pagos": pagos,
            "incidencias": incidencias,
            "stats": stats,
        },
    )

@login_required
def inquilino_panel(request):
    inquilinos = Inquilino.objects.filter(usuario=request.user).select_related("inmueble")
    inmuebles = (
        Inmueble.objects.filter(inquilinos__usuario=request.user)
        .distinct()
        .prefetch_related("incidencias", "pagos", "contratos")
    )
    contratos = (
        Contrato.objects.filter(inquilinos__usuario=request.user)
        .prefetch_related("inquilinos", "inmueble")
        .distinct()
    )
    pagos = (
        Pago.objects.filter(inmueble__in=inmuebles)
        .select_related("tipo", "inmueble")
        .order_by("-fecha")[:20]
    )
    incidencias = (
        Incidencia.objects.filter(inmueble__in=inmuebles)
        .select_related("inmueble")
        .order_by("-fecha_reporte")[:20]
    )
    stats = {
        "inmuebles": inmuebles.count(),
        "contratos": contratos.count(),
        "pagos_pendientes": Pago.objects.filter(
            inmueble__in=inmuebles, pagado=False
        ).count(),
        "incidencias_abiertas": Incidencia.objects.filter(
            inmueble__in=inmuebles, fecha_resolucion__isnull=True
        ).count(),
    }
    return render(
        request,
        "core/panel_inquilino.html",
        {
            "inquilinos": inquilinos,
            "inmuebles": inmuebles,
            "contratos": contratos,
            "pagos": pagos,
            "incidencias": incidencias,
            "stats": stats,
        },
    )

@login_required
def staff_panel(request):
    context = {
        "counts": {
            "propietarios": Propietario.objects.count(),
            "inquilinos": Inquilino.objects.count(),
            "inmuebles": Inmueble.objects.count(),
            "contratos": Contrato.objects.count(),
            "pagos": Pago.objects.count(),
            "incidencias": Incidencia.objects.count(),
        },
        "recent": {
            "inmuebles": Inmueble.objects.select_related("propietario").order_by("-id")[:10],
            "pagos": Pago.objects.select_related("inmueble", "tipo").order_by("-fecha")[:10],
            "incidencias": Incidencia.objects.select_related("inmueble").order_by("-fecha_reporte")[:10],
        },
    }
    return render(request, "core/panel_staff.html", context)

# --- Inmuebles ---
class InmuebleList(LoginRequiredMixin, ListView):
    model = Inmueble
    paginate_by = 20  # opcional
    ordering = ["direccion"]
    template_name = "core/inmueble_list.html"

class InmuebleDetail(LoginRequiredMixin, DetailView):
    model = Inmueble
    template_name = "core/inmueble_detail.html"

class InmuebleCreate(LoginRequiredMixin, CreateView):
    model = Inmueble
    form_class = InmuebleForm
    success_url = reverse_lazy("core:inmueble_list")
    template_name = "core/inmueble_form.html"

class InmuebleUpdate(LoginRequiredMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    success_url = reverse_lazy("core:inmueble_list")
    template_name = "core/inmueble_form.html"

class InmuebleDelete(LoginRequiredMixin, DeleteView):
    model = Inmueble
    success_url = reverse_lazy("core:inmueble_list")
    template_name = "core/inmueble_confirm_delete.html"

# --- Propietarios (ejemplo simple) ---
class PropietarioList(LoginRequiredMixin, ListView):
    model = Propietario
    ordering = ["nombre"]
    template_name = "core/propietario_list.html"

# --- Incidencias ---
class IncidenciaCreate(LoginRequiredMixin, CreateView):
    model = Incidencia
    form_class = IncidenciaForm
    template_name = "core/incidencia_form.html"
    success_url = reverse_lazy("core:inquilino_panel")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # The user is already passed to the form in get_form_kwargs
        return super().form_valid(form)
