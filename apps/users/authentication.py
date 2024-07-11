from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

    
#Agregamos tiempo de expiracion al token
class ExpiringTokenAuthentication(TokenAuthentication):
    
    def expires_in(self,token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time
    
    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)
    
    def token_expired_handler(self, token):
        is_expire = self.is_token_expired(token)
        #Actualizamos el token de forma automatica
        if is_expire:
            
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user = token.user)
        
        return token
        
    def authenticate_credentials(self, key):
        
        user = None
        try: 
            #Si encontro el token lo guardamos
            token = self.get_model().objects.select_related("user").get(key=key)
            token = self.token_expired_handler(token)
            user = token.user
        except self.get_model().DoesNotExist:
            pass
            
        return user
        
        