from django.db import models
from django.utils.timezone import now, datetime

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
    for r in range(1969, (datetime.now().year+1)):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField( 
        ('year'), choices=YEAR_CHOICES, default=datetime.now().year) 

def __str__(self):
        return self.name + ", " + str(self.year) + ", " + self.model_type

class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.address = address
        self.city = city
        self.full_name = full_name  # Full name of dealership
        self.id = id  # Dealership id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st  # State alpha code
        self.state = state  # Full state name
        self.zip = zip
        self.idx = 0

        def __str__(self):
            return self.full_name + ", " + self.state
        
class DealerReview:
    def __init__(self, dealership, id, name, purchase, review, car_make=None, car_year=None, purchase_date=None, sentiment="neutral"):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id  # The id of the review
        self.name = name  # Name of the reviewer
        self.purchase = purchase  # Did the reviewer purchase the car? bool
        self.purchase_date = purchase_date
        self.review = review  # The actual review text
        self.sentiment = sentiment  # Watson NLU sentiment 
    def __str__(self):
        return "Reviewer: " + self.name + " Review: " + self.review
        