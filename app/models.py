from django.db import models

# Create your models here.


class EnterpriseType(models.Model):
    type = models.CharField(max_length=64, unique=True)
