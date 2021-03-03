from django.db import models



class Brand(models.Model):
    cid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)


class Product(models.Model):
    cid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, blank=True, null=True)


class Sales(models.Model):
    check_id = models.CharField(max_length=100, blank=True, null=True)
    qty = models.DecimalField(max_digits=20, decimal_places=4)
    total_price = models.DecimalField(max_digits=20, decimal_places=4)
    product = models.ForeignKey(Product)
    store = models.ForeignKey('Store', blank=True, null=True)


class Store(models.Model):
    cid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

