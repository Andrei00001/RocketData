from django.db import models


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
    email = models.EmailField(max_length=64)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    the_outside = models.CharField(max_length=64)
    house_number = models.CharField(max_length=64)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='contacts')


class EnterpriseProducts(models.Model):
    name = models.CharField(max_length=25, unique=True)
    model = models.CharField(max_length=64)
    market_launch_date = models.DateField()
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='products')


class EnterpriseEmployees(models.Model):
    name = models.CharField(max_length=64)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='employees')


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
        super().save(*args, **kwargs)

