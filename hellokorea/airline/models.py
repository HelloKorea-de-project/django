from django.db import models
		
class CheapestFlight(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    depAirportCode = models.CharField(max_length=10, null=False)
    depCountryCode = models.CharField(max_length=10, null=False)
    currencyCode = models.CharField(max_length=10, null=False)
    arrAirportCode = models.CharField(max_length=10, null=False)
    carrierName = models.CharField(max_length=50, null=True)
    depTime = models.DateTimeField(null=True)
    arrTime = models.DateTimeField(null=True)
    price = models.FloatField(null=True)
    url = models.CharField(max_length=800, null=True)
    
class ExchangeRate(models.Model):
    currencyCode = models.CharField(max_length=10, unique=True, null=False)
    standardRate = models.FloatField(null=True)
    ttb = models.FloatField(null=True)
    tts = models.FloatField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
    updatedAt = models.DateTimeField(auto_now=True, null=False)

class Weather(models.Model):
    tm = models.DateField(primary_key=True)
    avgTa = models.FloatField(null=True)
    minTa = models.FloatField(null=True)
    maxTa = models.FloatField(null=True)
    sumRn = models.FloatField(null=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)