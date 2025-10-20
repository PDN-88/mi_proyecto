from django.shortcuts import render
from django.utils import timezone

from .models import Propietario, Inmueble, Inquilino, Contrato, Pago, Incidencia


def home(request):
    today = timezone.now().date()

    stats = {
        "propietarios": Propietario.objects.count(),
        "inmuebles": Inmueble.objects.count(),
        "inquilinos": Inquilino.objects.count(),
        "contratos": Contrato.objects.count(),
        "pagos_pendientes": Pago.objects.filter(pagado=False).count(),
    }

    pagos_recientes = (
        Pago.objects.select_related("inmueble", "tipo").order_by("-fecha")[:5]
    )
    incidencias_recientes = (
        Incidencia.objects.select_related("inmueble").order_by("-fecha_reporte")[:5]
    )

    context = {
        "stats": stats,
        "pagos_recientes": pagos_recientes,
        "incidencias_recientes": incidencias_recientes,
        "hoy": today,
    }
    return render(request, "core/home.html", context)
