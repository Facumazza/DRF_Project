from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel
from django.db.models import Sum

# Create your models here.

class MeasureUnit(BaseModel):

    description = models.CharField("Descripcion", max_length=50, blank=False, null=False, unique=True)
    historical = HistoricalRecords()
    
    @property
    def history_user(self):
        return self.changed_by
    
    @history_user.setter
    def _history_user(self, value):
        self.changed_by = value
    
    

    class Meta:
        verbose_name = ("Unidad de medida")
        verbose_name_plural = ("Unidades de medida")


    def __str__(self):
        return self.description
    
    
class CategoryProduct(BaseModel):
    
    description = models.CharField("Descripcion", max_length=50, unique=True, blank=False, null=False)
    historical = HistoricalRecords()
    
    @property
    def history_user(self):
        return self.changed_by
    
    @history_user.setter
    def _history_user(self, value):
        self.changed_by = value
    

    class Meta:
        verbose_name = ("Categoria del productos")
        verbose_name_plural = ("Categorias de los productos")

    def __str__(self):
        return self.description

    


class Indicator(BaseModel):
    
    descount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name="Indicador de oferta")
    historical = HistoricalRecords()
    
    @property
    def history_user(self):
        return self.changed_by
    
    @history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = ("Indicador de oferta")
        verbose_name_plural = ("Indicadores de oferta")

    def __str__(self):
        return f"Oferta de la categoria {self.category_product}: {self.descount_value}%"
    
    
class Product(BaseModel):

    name = models.CharField(max_length=150, unique=True, blank=False, null= False)
    description = models.TextField("Descripcion del producto", blank=False, null=False)
    image = models.ImageField("Imagen del producto", upload_to="products/", blank=True, null=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name="Unidad de medida", null=True)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name="Categoria del producto", null=True)
    historical = HistoricalRecords()
    
    @property
    def history_user(self):
        return self.changed_by
    
    @history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")

    def __str__(self):
        return self.name
    
    @property
    def stock(self):
        from apps.expense_manager.models import Expense

        expense = Expense.objects.filter(
            product = self,
            state = True
        ).aggregate(Sum("quantity"))
        
        return expense
        





