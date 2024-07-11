from faker import Faker

from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User

class TestSetUp(APITestCase):
    
    #Creamos una sesion de prueba con su token para poder accionar como superuser
    def setUp(self):
        #Nos permite crear datos de prueba
        faker = Faker()
        
        self.login_url = "/login/"
        self.user = User.objects.create_superuser(
            name = "Facundo",
            last_name = "Mazza",
            username = faker.name(),
            password = "PruebaUnitaria",
            email = faker.email()
        )
        
        #simulador de peticiones como Postman
        response = self.client.post(
            self.login_url,
            {
                "username": self.user.username,
                "password": "PruebaUnitaria"
            },
            format= "json"
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)
        #self.token = response.data["token"]
        #self.client.credentials(HTTTP_AUTHORIZATION="Bearer" + self.token)
        return super().setUp()
    
    