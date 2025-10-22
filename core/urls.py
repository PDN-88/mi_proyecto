from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    # Inmuebles (CRUD básico)
    path("inmuebles/", views.InmuebleList.as_view(), name="inmueble_list"),
    path("inmuebles/<int:pk>/", views.InmuebleDetail.as_view(), name="inmueble_detail"),
    path("inmuebles/crear/", views.InmuebleCreate.as_view(), name="inmueble_create"),
    path("inmuebles/<int:pk>/editar/", views.InmuebleUpdate.as_view(), name="inmueble_update"),
    path("inmuebles/<int:pk>/borrar/", views.InmuebleDelete.as_view(), name="inmueble_delete"),

    # Propietarios (solo lista para empezar)
    path("propietarios/", views.PropietarioList.as_view(), name="propietario_list"),
]
