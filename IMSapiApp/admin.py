from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Vendor, Purchase, Sale, Inventory


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'vendor']


class AdminVendor(admin.ModelAdmin):
    list_display = ['username']


class AdminPurchase(admin.ModelAdmin):
    list_display = ['product', 'vendor', 'pur_quantity', 'total_price']


class AdminSale(admin.ModelAdmin):
    list_display = ['product', 'vendor', 'sale_quantity', 'total_price']


class AdminInventory(admin.ModelAdmin):
    list_display = ['product', 'vendor', 'total_pur_quantity',
                    'total_sale_quantity', 'in_stock']


# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Vendor, AdminVendor)
admin.site.register(Purchase, AdminPurchase)
admin.site.register(Sale, AdminSale)
admin.site.register(Inventory, AdminInventory)
