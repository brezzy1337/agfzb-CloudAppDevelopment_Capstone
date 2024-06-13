from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100)
    description = models.TextField(null=True, max_length=500)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=99)
    dealer_id = models.IntegerField(null=True)
 
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('CONVERTIBLE', 'Convertible'),
    ]
    model_type = models.CharField(null=False, max_length=19, choices=TYPE_CHOICES, default="SEDAN")

    YEAR_CHOICES = []
    for r in range(1969, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField( 
        ('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year) 

def __str__(self):
        return self.name + ", " + str(self.year) + ", " + self.model_type