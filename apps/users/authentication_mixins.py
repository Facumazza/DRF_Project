from rest_framework.authentication import get_authorization_header
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, authentication, exceptions

from apps.users.authentication import ExpiringTokenAuthentication


#Es una autenticación personalizada
class Authentication(authentication.BaseAuthentication):
    user = None
    
    
    
    #aca obtenemos el token decodificado
    def get_user(self, request):
        token = get_authorization_header(request).split()
        
        if token:
            try:
                token = token[1].decode()
                
            except:    
                return None
            
            token_expire = ExpiringTokenAuthentication()
            #Esto ejecuta la función authenticate_credentials y lo valida
            user = token_expire.authenticate_credentials(token)    
                 
            if user != None:
                self.user = user
                return user
               
        
        return None
    
    def authenticate(self, request):
        self.get_user(request)
        if self.user is None:
            raise exceptions.AuthenticationFailed("La usuario o contraseña es incorrecto.")
        
        return (self.user, None)

        
        