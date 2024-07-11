from rest_framework.routers import DefaultRouter
from apps.products.api.viewsets.general_views import *
from apps.expense_manager.api.viewsets.expense_viewsets import ExpenseViewSet

router = DefaultRouter()

router.register(r"expense", ExpenseViewSet, basename="expense")


urlpatterns = router.urls
