from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
import pytz
from airline.models import AirportInformation, ExchangeRate, CheapestFlight, ArrCountToICN, Weather, ServiceAirportICN

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        AirportInformation.objects.all().delete()
        ExchangeRate.objects.all().delete()
        CheapestFlight.objects.all().delete()
        ArrCountToICN.objects.all().delete()
        Weather.objects.all().delete()
        ServiceAirportICN.objects.all().delete()

        # Dummy data for AirportInformation
        airports = [
            {"airportCode": "ICN", "countryCode": "KR", "currencyCode": "KRW"},
            {"airportCode": "JFK", "countryCode": "US", "currencyCode": "USD"},
            {"airportCode": "LAX", "countryCode": "US", "currencyCode": "USD"},
            {"airportCode": "NRT", "countryCode": "JP", "currencyCode": "JPY"}
        ]
        for airport in airports:
            airport_info = AirportInformation(**airport)
            airport_info.save()

        # Dummy data for ServiceAirportICN
        for airport in airports:
            service_airport = ServiceAirportICN(**airport)
            service_airport.save()

        # Dummy data for ExchangeRate
        currencies = ["KRW", "USD", "JPY", "EUR"]
        for currency in currencies:
            exchange_rate = ExchangeRate(
                currencyCode=currency,
                standardRate=random.uniform(0.8, 1500),
                ttb=random.uniform(0.7, 1490),
                tts=random.uniform(0.9, 1510)
            )
            exchange_rate.save()

        kst = pytz.timezone('Asia/Seoul')

        # Dummy data for CheapestFlight
        for i in range(1, 6):
            cheapest_flight = CheapestFlight(
                id=f"FL{i:03d}",
                depAirportCode=random.choice(["ICN", "JFK", "LAX", "NRT"]),
                currencyCode=random.choice(["KRW", "USD", "JPY"]),
                arrAirportCode=random.choice(["ICN", "JFK", "LAX", "NRT"]),
                carrierName=random.choice(["Korean Air", "Delta", "ANA", "United"]),
                depTime=timezone.make_aware(datetime(2024, 8, i, 10, 0), kst),
                arrTime=timezone.make_aware(datetime(2024, 8, i, 18, 0), kst),
                price=random.uniform(100.0, 2000.0),
                url=f"http://example.com/flight/FL{i:03d}"
            )
            cheapest_flight.save()

        # Dummy data for ArrCountToICN
        for airport_code in ["JFK", "LAX", "NRT"]:
            arr_count = ArrCountToICN(
                airportCode=airport_code,
                count=random.randint(1, 10)
            )
            arr_count.save()

        # Dummy data for Weather
        base_date = datetime(2024, 7, 20)
        for i in range(10):
            weather = Weather(
                tm=(base_date + timedelta(days=i)).date(),
                avgTa=random.uniform(20.0, 30.0),
                minTa=random.uniform(15.0, 25.0),
                maxTa=random.uniform(25.0, 35.0),
                sumRn=random.uniform(0.0, 100.0)
            )
            weather.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))
