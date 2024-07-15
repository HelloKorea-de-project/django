from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    arrival_date = models.DateField()

    def __str__(self):
        return f"{self.flight_number} from {self.departure_city} to {self.arrival_city}"
