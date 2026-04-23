from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Bill(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

class Sale(models.Model):
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product