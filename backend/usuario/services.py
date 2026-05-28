from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from core.tokens import create_access_token

from .models import Usuario
from .repositories import UsuarioRepository


@dataclass(frozen=True)
class AuthResult:
    token: str
    usuario: Usuario


class UsuarioAuthService:
    def __init__(self, repository: UsuarioRepository | None = None):
        self.repository = repository or UsuarioRepository()

    def authenticate(self, correo: str, password: str) -> AuthResult:
        usuario = self.repository.get_by_correo(correo)
        if usuario is None or not check_password(password, usuario.password):
            raise AuthenticationFailed('Credenciales invalidas.')

        if usuario.estado != 'activo':
            raise AuthenticationFailed('La cuenta se encuentra inactiva.')

        token = create_access_token(usuario.id)
        return AuthResult(token=token, usuario=usuario)


class UsuarioValidationService:
    def __init__(self, repository: UsuarioRepository | None = None):
        self.repository = repository or UsuarioRepository()

    def validate_correo_unico(self, correo: str, exclude_id: int | None = None):
        if self.repository.exists_correo(correo=correo, exclude_id=exclude_id):
            raise ValidationError({'correo': 'Ya existe un usuario con este correo.'})
