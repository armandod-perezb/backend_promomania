from __future__ import annotations

from django.db.models import QuerySet

from .models import Usuario


class UsuarioRepository:
    @staticmethod
    def get_queryset() -> QuerySet[Usuario]:
        return Usuario.objects.all().order_by('id')

    @staticmethod
    def get_by_correo(correo: str) -> Usuario | None:
        normalized = correo.strip().lower()
        return Usuario.objects.filter(correo__iexact=normalized).first()

    @staticmethod
    def exists_correo(correo: str, exclude_id: int | None = None) -> bool:
        qs = Usuario.objects.filter(correo__iexact=correo.strip().lower())
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        return qs.exists()
