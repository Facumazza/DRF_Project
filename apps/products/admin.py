from django.contrib import admin
from apps.products.models import *
# Register your models here.

class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ("id", "description")
    
class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ("id", "description")
    
admin.site.register(MeasureUnit, MeasureUnitAdmin)
admin.site.register(Indicator)
admin.site.register(Product)
admin.site.register(CategoryProduct, CategoryProductAdmin)
