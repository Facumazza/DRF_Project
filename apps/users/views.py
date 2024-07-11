from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.api.serializers import CustomTokenObtainPairSerializer, CustomUserSerializer, LogoutSerializer  


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        
        # Autenticar al usuario
        user = authenticate(username=username, password=password)
        
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    "token": login_serializer.validated_data.get("access"),
                    "refresh-token": login_serializer.validated_data.get("refresh"),
                    "user": user_serializer.data,
                    "message": "Inicio de sesión exitoso.",
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "Credenciales inválidas. Por favor, intenta de nuevo."
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "error": "Credenciales inválidas. Por favor, intenta de nuevo."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
class Logout(GenericAPIView):
    serializer_class = LogoutSerializer  
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Extrae el token de refresco desde los datos validados
            refresh_token = serializer.validated_data.get("refresh")
            token = RefreshToken(refresh_token)
            
            # Verificar que el token de refresco pertenece al usuario autenticado
            if token.payload["user_id"] != request.user.id:
                return Response({"error": "No autorizado para cerrar esta sesión."}, status=status.HTTP_403_FORBIDDEN)
            
            # Añadir el token a la lista negra
            token.blacklist()

            return Response({"message": "Sesión cerrada correctamente."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "No se pudo cerrar la sesión correctamente."}, status=status.HTTP_400_BAD_REQUEST)
            
                