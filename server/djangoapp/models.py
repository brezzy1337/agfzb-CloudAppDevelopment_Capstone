from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=99)

 
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('CONVERTIBLE', 'Convertible'),
    ]
    type = models.CharField(max_length=19, choices=TYPE_CHOICES, default="SEDAN")
    year = models.IntegerField(default=2023) 

def __str__(self):
        return self.name  # Return the name as the string representation
