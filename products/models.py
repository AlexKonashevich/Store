from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    discription = models.TextField(null=True, blank=True)
