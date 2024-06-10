from django.contrib import admin
from .models import CarMake, CarModel

#Registering Models with Admin
admin.site.register(CarMake)
admin.site.register(CarModel)
