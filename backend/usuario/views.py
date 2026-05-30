from core.views import BaseModelViewSet
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Usuario
from .serializers import (
    AuthResponseSerializer,
    LoginSerializer,
    UsuarioSerializer,
)
from .services import UsuarioAuthService


auth_service = UsuarioAuthService()


class UsuarioViewSet(BaseModelViewSet):
    model = Usuario
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()


class AuthLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from rest_framework.exceptions import AuthenticationFailed as DRFAuthFailed
        try:
            result = auth_service.authenticate(
                correo=serializer.validated_data['correo'],
                password=serializer.validated_data['password'],
            )
        except DRFAuthFailed as exc:
            return Response(
                {'detail': str(exc.detail)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response_data = {
            'token': result.token,
            'usuario': UsuarioSerializer(result.usuario).data,
        }
        return Response(
            AuthResponseSerializer(response_data).data,
            status=status.HTTP_200_OK,
        )


class AuthMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UsuarioSerializer(request.user).data, status=status.HTTP_200_OK)
