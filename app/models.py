from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class EnterpriseType(models.Model):
    type = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.type


class Enterprise(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(EnterpriseType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class EnterpriseContacts(models.Model):
    email = models.EmailField(max_length=32)
    country = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    the_outside = models.CharField(max_length=32)
    house_number = models.CharField(max_length=32)
    enterprise = models.OneToOneField(Enterprise, on_delete=models.CASCADE, related_name='contacts')


class Products(models.Model):
    name = models.CharField(max_length=25, unique=True)
    model = models.CharField(max_length=64)
    market_launch_date = models.DateField()

    def __str__(self):
        return self.name


class EnterpriseProducts(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='enterprise')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.products.name


class EnterpriseEmployees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enterprise_user')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='user')


class SupplyChain(models.Model):
    provider = models.ForeignKey(Enterprise, on_delete=models.PROTECT, related_name='provider')
    recipient = models.ForeignKey(Enterprise, on_delete=models.PROTECT, related_name='recipient')
    price = models.FloatField(null=True, blank=True)
    move_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("provider", "recipient"),)

    def save(self, *args, **kwargs):
        if self.price is not None:
            self.price = round(self.price, 2)
        self.price = 0 if self.price < 0 else self.price
        super().save(*args, **kwargs)


class SupplyChainProducts(models.Model):
    supply_chain = models.ForeignKey(SupplyChain, on_delete=models.CASCADE, related_name='products_supply_chain')
    products = models.ForeignKey(EnterpriseProducts, on_delete=models.CASCADE, related_name='supply_chain')
