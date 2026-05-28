from __future__ import annotations

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from usuario.models import Usuario

from .tokens import TokenError, decode_access_token


class UsuarioTokenAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth:
            return None

        if auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) != 2:
            raise AuthenticationFailed('Formato de token invalido.')

        raw_token = auth[1].decode('utf-8')

        try:
            payload = decode_access_token(raw_token)
        except TokenError as exc:
            raise AuthenticationFailed(str(exc)) from exc

        usuario_id = payload.get('uid')
        if not usuario_id:
            raise AuthenticationFailed('Token sin identificador de usuario.')

        try:
            usuario = Usuario.objects.get(pk=usuario_id, estado='activo')
        except Usuario.DoesNotExist as exc:
            raise AuthenticationFailed('Usuario no encontrado o inactivo.') from exc

        return (usuario, raw_token)

    def authenticate_header(self, request):
        return self.keyword
