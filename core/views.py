# Create your views here.
# core/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Inmueble, Propietario
from .forms import InmuebleForm

@login_required

def home(request):
    return render(request, "home.html")

def user_in_group(user, name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name__iexact=name).exists()

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
