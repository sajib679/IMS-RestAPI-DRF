from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializer import ProductSerializer, VendorSerializer, PurchaseSerializer, SaleSerializer, InventorySerializer, CustomTokenObtainPairSerializer
from .models import Vendor, Product, Purchase, Sale, Inventory
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.filter(isVendor=True)
    serializer_class = VendorSerializer

    # def get_queryset(self):
    #     super(ProductViewSet, self).get_queryset()
    #     vendor = self.request.query_params.get('vendor', None)
    #     queryset = Product.objects.all()
    #     if vendor:
    #         queryset = Product.objects.filter(vendor=vendor)
    #     return queryset


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        super(ProductViewSet, self).get_queryset()
        vendor = self.request.query_params.get('vendor', None)
        queryset = Product.objects.all()
        if vendor:
            queryset = Product.objects.filter(vendor=vendor)
        return queryset


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_inventory_by_product_id(self, product):

        try:
            inventory = Inventory.objects.get(product=product)
        except Inventory.DoesNotExist:
            inventory = None
        return inventory

    def create(self, request, *args, **kwargs):
        pur_serializer = PurchaseSerializer(data=request.data)
        if pur_serializer.is_valid():
            pur_serializer.save()

        # Inventory Effect of Purchase
            inventory = self.get_inventory_by_product_id(
                product=request.data["product"])
            if inventory:
                pur_quantity = int(request.data["pur_quantity"])
                total_price = int(request.data["total_price"])
                print(total_price)
                total_pur_quantity = inventory.total_pur_quantity + pur_quantity
                total_pur_price = inventory.total_pur_price + total_price
                in_stock = inventory.in_stock + pur_quantity

                data = {"total_pur_quantity": total_pur_quantity, "total_pur_price": total_pur_price,
                        "in_stock": in_stock}

                inv_serializer = InventorySerializer(
                    inventory, data=data, partial=True)

                if inv_serializer.is_valid():
                    inv_serializer.save()
            else:
                pur_quantity = int(request.data["pur_quantity"])
                total_pur_quantity = pur_quantity
                total_price = int(request.data["total_price"])
                total_pur_price = total_price
                in_stock = pur_quantity
                product = request.data["product"]
                vendor = request.data["vendor"]

                inv_data = {"product": product,
                            "vendor": vendor,
                            "total_pur_quantity": total_pur_quantity,
                            "total_pur_price": total_pur_price,
                            "in_stock": in_stock,
                            "total_sale_quantity": 0,
                            }

                inv_serializer = InventorySerializer(data=inv_data)
                if inv_serializer.is_valid():
                    inv_serializer.save()

            return Response(pur_serializer.data)
        else:
            return Response(pur_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_inventory_by_product_id(self, product):

        try:
            inventory = Inventory.objects.get(product=product)
        except Inventory.DoesNotExist:
            inventory = None
        return inventory

    def create(self, request, *args, **kwargs):

        # Inventory Effect of Sale
        inventory = self.get_inventory_by_product_id(
            product=request.data["product"])
        if inventory:
            sale_quantity = int(request.data["sale_quantity"])
            total_price = int(request.data["total_price"])
            # Inventory quantity Check for sale

            if sale_quantity <= inventory.in_stock:
                # Sale instance saving
                sale_serializer = SaleSerializer(data=request.data)
                if sale_serializer.is_valid():
                    sale_serializer.save()
                    total_sale_quantity = inventory.total_sale_quantity+sale_quantity
                    total_sale_price = inventory.total_sale_price+total_price
                    in_stock = inventory.in_stock-sale_quantity
                    data = {"total_sale_quantity": total_sale_quantity,
                            "total_sale_price": total_sale_price,
                            "in_stock": in_stock}

                    inv_serializer = InventorySerializer(
                        inventory, data=data, partial=True)

                    if inv_serializer.is_valid():
                        inv_serializer.save()
                return Response(data={'sale': sale_serializer.data, 'inv': inv_serializer.data})

            else:
                return Response("Sale quantity should be less than or equal to stock", status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


# class VendorView(APIView):
#     def get_vendor_by_id(self, id):
#         return Vendor.objects.get(id=id)

#     def get(self, request):
#         queryset = Vendor.objects.all()
#         serializer = VendorSerializer(queryset, many=True)
#         return Response(queryset.data)

#     def post(self, request):
#         serializer = VendorSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request):

#         # print(list(request.data.items()))
#         # print(dict(request.data.items()))
#         query_object = self.get_vendor_by_id(request.data["id"])
#         serializer = VendorSerializer(
#             query_object, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request):
#         query_object = self.get_vendor_by_id(request.data["id"])
#         serializer = VendorSerializer(query_object)
#         print(serializer.data)
#         query_object.delete()
#         return Response({"message": "Deleted Succesfully", "data": serializer.data})


# class ProductView(APIView):

#     def get_product_by_id(self, id):
#         return Product.objects.get(id=id)

#     def get_product_by_brand_id(self, id):
#         return Product.objects.get(brand_id=id)

#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request):

#         # print(list(request.data.items()))
#         # print(dict(request.data.items()))
#         query_object = self.get_product_by_id(request.data["id"])
#         serializer = ProductSerializer(
#             query_object, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request):
#         query_object = self.get_product_by_id(request.data["id"])
#         serializer = ProductSerializer(query_object)
#         print(serializer.data)
#         query_object.delete()
#         return Response({"message": "Deleted Succesfully", "data": serializer.data})
