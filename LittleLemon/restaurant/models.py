from django.db import models
from datetime import datetime
from decimal import Decimal
# Create your models here.
class Booking(models.Model):
    ID = models.IntegerField(primary_key=True,)
    Name = models.CharField(max_length=255)
    No_of_guests = models.IntegerField()
    Bookingdate = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self) -> str:
        return self.Name


class Menu(models.Model):
    ID = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default = 0.0 )
    Inventory = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.Title}:{self.price}'