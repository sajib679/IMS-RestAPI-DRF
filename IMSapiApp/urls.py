
from django.contrib import admin
from django.urls import path, include
from .views import VendorViewSet, ProductViewSet, PurchaseViewSet, SaleViewSet, InventoryViewSet, CustomTokenObtainPairView
from rest_framework.routers import DefaultRouter

# Router Object
router = DefaultRouter()

router.register('vendor', VendorViewSet, basename='vendor')
router.register('product', ProductViewSet, basename='product')
router.register('purchase', PurchaseViewSet, basename='purchase')
router.register('sale', SaleViewSet, basename='sale')
router.register('inventory', InventoryViewSet, basename='inventory')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view()),
]
