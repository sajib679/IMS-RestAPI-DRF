
from rest_framework import serializers
from .models import Product, Purchase, Vendor, Inventory, Sale
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['isVendor'] = user.isVendor
        token['isSuperuser'] = user.is_superuser

        return token


class VendorSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Vendor
        fields = ["id", "username", "email",
                  "password", "isVendor", "is_superuser"]
        # write_only_fields = ('password')
        read_only_fields = ("id", "isVendor", "is_superuser")

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if Vendor.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('email already exists')})
        if Vendor.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': ('vendor already exists')})
        return super().validate(args)

    def create(self, validated_data):
        return Vendor.objects.create_user(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    # vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        product = super(ProductSerializer, self).to_representation(instance)
        product["vendor"] = {"id": instance.vendor.id,
                             "name": instance.vendor.username}
        return product


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

    def to_representation(self, instance):
        purchase = super(PurchaseSerializer, self).to_representation(instance)
        purchase["vendor"] = {"id": instance.vendor.id,
                              "name": instance.vendor.username}
        purchase["product"] = {"id": instance.product.id,
                               "name": instance.product.name,
                               "vendor": instance.product.vendor.username
                               }
        return purchase


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

    def to_representation(self, instance):
        sale = super(SaleSerializer, self).to_representation(instance)
        sale["vendor"] = {"id": instance.vendor.id,
                          "name": instance.vendor.username}
        sale["product"] = {"id": instance.product.id,
                           "name": instance.product.name,
                           }
        return sale


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

    def to_representation(self, instance):
        inventory = super(InventorySerializer,
                          self).to_representation(instance)
        inventory["vendor"] = {"id": instance.vendor.id,
                               "name": instance.vendor.username}
        inventory["product"] = {"id": instance.product.id,
                                "name": instance.product.name,
                                "price": instance.product.price}
        return inventory
