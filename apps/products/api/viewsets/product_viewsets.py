from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from apps.products.api.serializers.product_serializer import ProductSerializer
from apps.base.utils import validate_files

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state = True)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk, state = True).first()
        
    def list(self,request):
        product_serializer = self.get_serializer(self.get_queryset(), many= True)
        return Response(product_serializer.data, status = status.HTTP_200_OK)
        
    def create(self, request):
        #Enviamos información al serializador
        data = validate_files(request.data, "image")
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Producto creado correctamente"}, status= status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk = None):
        if self.get_queryset(pk):
            data = validate_files(request.data, "image", True)
            product_serializer = self.serializer_class(self.get_queryset(pk), data = data)
            
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status= status.HTTP_200_OK)
            return Response(product_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        product = self.get_object()
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
    #Eliminacion logica
    def destroy(self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response({"message": "Producto eliminado correctamente"}, status=status.HTTP_200_OK)
        
        return Response({"error": "No existe un producto con estos datos"}, status= status.HTTP_400_BAD_REQUEST)      
    

    
    
    
      
    
      
    
    
    
      
            
        
        
    
    