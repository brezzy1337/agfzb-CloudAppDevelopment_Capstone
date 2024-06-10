from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=99)
    type = models.CharField(max_length=19, choices=TYPE_CHOICES, default=SEDAN)
    year = models.IntergerField(default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]) 
 
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('CONVERTIBLE', 'Convertible'),
    ]

def __str__(self):
