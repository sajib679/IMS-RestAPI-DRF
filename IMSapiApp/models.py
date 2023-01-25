
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Vendor


class CustomVendorManager(BaseUserManager):

    def create_superuser(self, email, username, password,  **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('isVendor', False)
        other_fields.setdefault('is_staff', True)
        email = self.normalize_email(email)
        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):
        email = self.normalize_email(email)
        vendor = self.model(email=email, username=username,
                            **other_fields)
        vendor.set_password(password)
        vendor.save()
        return vendor


class Vendor(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250, unique=True)
    isVendor = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomVendorManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


# Product
class Product(models.Model):
    name = models.CharField(max_length=500)
    price = models.FloatField()
    quantity = models.IntegerField()
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]


# Purchase
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    pur_quantity = models.IntegerField(default=0)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ["-id"]


# Sale
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    price = models.FloatField()
    sale_quantity = models.IntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ["-id"]


# Inventory
class Inventory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE)
    total_pur_quantity = models.IntegerField(default=0)
    total_pur_price = models.IntegerField(default=0)
    total_sale_quantity = models.IntegerField(default=0)
    total_sale_price = models.IntegerField(default=0)
    in_stock = models.IntegerField(default=0)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Inventories'
        ordering = ["date_modified"]
