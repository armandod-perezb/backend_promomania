# Backend Promomania

API REST construida con Django + DRF para la app móvil Promomania.

## Arquitectura aplicada

- `views`: capa HTTP (controladores).
- `serializers`: validación/transformación de datos de entrada/salida.
- `services`: reglas de negocio (casos de uso).
- `repositories`: acceso a datos y consultas.

Implementado de forma explícita en:
- `usuario` (autenticación y validaciones de correo).
- `promocion` (filtros y reglas de vigencia/precio/descuento).

## Endpoints clave para Flutter

- `GET /api/health/`
- `POST /api/auth/login/`
- `GET /api/auth/me/` (requiere `Authorization: Bearer <token>`)
- CRUD estándar en `/api/usuarios/`, `/api/promociones/`, etc.

Filtros de promociones:
- `GET /api/promociones/?estado=aprobada`
- `GET /api/promociones/?categoria_id=1`
- `GET /api/promociones/?supermercado_id=2`
- `GET /api/promociones/?usuario_id=10`
- `GET /api/promociones/?q=arroz`

## Variables de entorno

Usa `.env.example` como base para tu configuración local o Docker.
