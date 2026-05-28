from __future__ import annotations

from django.conf import settings
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired


class TokenError(Exception):
    """Raised when a bearer token is malformed or expired."""


_TOKEN_SALT = 'promomania.api.auth'


def create_access_token(usuario_id: int) -> str:
    payload = {'uid': usuario_id}
    return signing.dumps(payload, salt=_TOKEN_SALT)


def decode_access_token(token: str) -> dict:
    max_age = getattr(settings, 'API_TOKEN_TTL_SECONDS', 60 * 60 * 24 * 7)
    try:
        return signing.loads(token, salt=_TOKEN_SALT, max_age=max_age)
    except SignatureExpired as exc:
        raise TokenError('El token ha expirado.') from exc
    except BadSignature as exc:
        raise TokenError('El token no es valido.') from exc
