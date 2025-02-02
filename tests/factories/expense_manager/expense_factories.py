from faker import Faker

from apps.expense_manager.models import Supplier

faker = Faker()

class SupplierFactory:

    #Creamos un supplier para los tests
    def build_supplier_JSON(self):
        return {
            'ruc': str(faker.random_number(digits=11)),
            'business_name': faker.company(),
            'address': faker.address(),
            'phone': str(faker.random_number(digits=11)),
            'email': faker.email()
        }

    def create_supplier(self):
        return Supplier.objects.create(**self.build_supplier_JSON())