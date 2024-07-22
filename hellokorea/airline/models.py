from django.db import models
from django.utils import timezone
import pytz

class AirportInformation(models.Model):
    airportCode = models.CharField(max_length=10, unique=True, null=False)
    countryName = models.CharField(max_length=50, null=False)
    currency = models.CharField(max_length=10, null=False)

class ExchangeRate(models.Model):
    createdAtKST = models.DateTimeField(auto_now_add=True, null=False)
    currency = models.CharField(max_length=10, unique=True, null=False)
    standardRate = models.FloatField(null=True)
    ttb = models.FloatField(null=True)
    tts = models.FloatField(null=True)

class CheapestFlight(models.Model):
    flightID = models.CharField(max_length=50, primary_key=True)
    depAirport = models.CharField(max_length=10, null=False)
    depCountryName = models.CharField(max_length=50, null=False)
    currency = models.CharField(max_length=10, null=False)
    arrAirport = models.CharField(max_length=10, null=False)
    carrier = models.CharField(max_length=50, null=True)
    depTimeUTC = models.DateTimeField(null=True)
    arrTimeUTC = models.DateTimeField(null=True)
    price = models.FloatField(null=True)
    url = models.CharField(max_length=200, null=True)
    createdDateKST = models.DateField(null=True)
    createdAtKST = models.DateTimeField(auto_now_add=True, null=False)
    updatedAtKST = models.DateTimeField(auto_now=True, null=False)

class ArrCountToICN(models.Model):
    createdAtKST = models.DateTimeField(auto_now_add=True, null=False)
    updatedAtKST = models.DateTimeField(auto_now=True, null=False)
    depAirport = models.CharField(max_length=10, unique=True, null=False)
    count = models.IntegerField(null=False, default=0)

class Weather(models.Model):
    tmKST = models.DateField(primary_key=True)
    avgTa = models.FloatField(null=True)
    minTa = models.FloatField(null=True)
    maxTa = models.FloatField(null=True)
    sumRn = models.FloatField(null=True)
    createdAtKST = models.DateTimeField(auto_now_add=True, null=False)
    updatedAtKST = models.DateTimeField(auto_now=True, null=False)
