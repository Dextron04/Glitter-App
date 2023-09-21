from django.db import models

class TableModel(models.Model):
    number = models.IntegerField()
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.IntegerField()
    expiration_date = models.DateField()
