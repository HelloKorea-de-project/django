# from django.core.management.base import BaseCommand
# from airline.models import AirportInformation, ExchangeRate, CheapestFlight, ArrCountToICN, Weather
# from datetime import datetime, timedelta
# import pytz
# import random

# class Command(BaseCommand):
#     help = 'Populate the database with dummy data'

#     def handle(self, *args, **kwargs):
#         # Clear existing data
#         AirportInformation.objects.all().delete()
#         ExchangeRate.objects.all().delete()
#         CheapestFlight.objects.all().delete()
#         ArrCountToICN.objects.all().delete()
#         Weather.objects.all().delete()

#         # Dummy data for AirportInformation
#         airports = [
#             {"airportCode": "ICN", "countryName": "South Korea", "currency": "KRW"},
#             {"airportCode": "JFK", "countryName": "United States", "currency": "USD"},
#             {"airportCode": "LAX", "countryName": "United States", "currency": "USD"},
#             {"airportCode": "NRT", "countryName": "Japan", "currency": "JPY"}
#         ]
#         for airport in airports:
#             AirportInformation.objects.create(**airport)

#         # Dummy data for ExchangeRate
#         currencies = ["KRW", "USD", "JPY", "EUR"]
#         for currency in currencies:
#             ExchangeRate.objects.create(
#                 currency=currency,
#                 standardRate=random.uniform(0.8, 1500),
#                 ttb=random.uniform(0.7, 1490),
#                 tts=random.uniform(0.9, 1510)
#             )

#         # Dummy data for CheapestFlight
#         for i in range(1, 6):
#             CheapestFlight.objects.create(
#                 flightID=f"FL{i:03d}",
#                 depAirport=random.choice(["ICN", "JFK", "LAX", "NRT"]),
#                 depCountryName=random.choice(["South Korea", "United States", "Japan"]),
#                 currency=random.choice(["KRW", "USD", "JPY"]),
#                 arrAirport=random.choice(["ICN", "JFK", "LAX", "NRT"]),
#                 carrier=random.choice(["Korean Air", "Delta", "ANA", "United"]),
#                 depTimeUTC=datetime(2024, 8, i, 10, 0, tzinfo=pytz.UTC),
#                 arrTimeUTC=datetime(2024, 8, i, 18, 0, tzinfo=pytz.UTC),
#                 price=random.uniform(100.0, 2000.0),
#                 url=f"http://example.com/flight/FL{i:03d}",
#                 createdDateKST=datetime(2024, 7, 20).date()
#             )

#         # Dummy data for ArrCountToICN
#         for airport_code in ["JFK", "LAX", "NRT"]:
#             ArrCountToICN.objects.create(
#                 depAirport=airport_code,
#                 count=random.randint(1, 10)
#             )

#         # Dummy data for Weather
#         base_date = datetime(2024, 7, 20)
#         for i in range(10):
#             Weather.objects.create(
#                 tmKST=(base_date + timedelta(days=i)).date(),
#                 avgTa=random.uniform(20.0, 30.0),
#                 minTa=random.uniform(15.0, 25.0),
#                 maxTa=random.uniform(25.0, 35.0),
#                 sumRn=random.uniform(0.0, 100.0)
#             )

#         self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))


from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
import pytz
from airline.models import AirportInformation, ExchangeRate, CheapestFlight, ArrCountToICN, Weather

class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        AirportInformation.objects.all().delete()
        ExchangeRate.objects.all().delete()
        CheapestFlight.objects.all().delete()
        ArrCountToICN.objects.all().delete()
        Weather.objects.all().delete()

        # Dummy data for AirportInformation
        airports = [
            {"airportCode": "ICN", "countryName": "South Korea", "currency": "KRW"},
            {"airportCode": "JFK", "countryName": "United States", "currency": "USD"},
            {"airportCode": "LAX", "countryName": "United States", "currency": "USD"},
            {"airportCode": "NRT", "countryName": "Japan", "currency": "JPY"}
        ]
        for airport in airports:
            airport_info = AirportInformation(**airport)
            airport_info.save()

        # Dummy data for ExchangeRate
        currencies = ["KRW", "USD", "JPY", "EUR"]
        for currency in currencies:
            exchange_rate = ExchangeRate(
                currency=currency,
                standardRate=random.uniform(0.8, 1500),
                ttb=random.uniform(0.7, 1490),
                tts=random.uniform(0.9, 1510)
            )
            exchange_rate.save()

        kst = pytz.timezone('America/Chicago')

        # Dummy data for CheapestFlight
        for i in range(1, 6):
            cheapest_flight = CheapestFlight(
                flightID=f"FL{i:03d}",
                depAirport=random.choice(["ICN", "JFK", "LAX", "NRT"]),
                depCountryName=random.choice(["South Korea", "United States", "Japan"]),
                currency=random.choice(["KRW", "USD", "JPY"]),
                arrAirport=random.choice(["ICN", "JFK", "LAX", "NRT"]),
                carrier=random.choice(["Korean Air", "Delta", "ANA", "United"]),
                # depTimeUTC=timezone.make_aware(datetime(2024, 8, i, 10, 0), pytz.utc),
                # arrTimeUTC=timezone.make_aware(datetime(2024, 8, i, 18, 0), pytz.utc),
                depTimeUTC=kst.localize(datetime(2024, 8, i, 10, 0)),
                arrTimeUTC=kst.localize(datetime(2024, 8, i, 18, 0)),
                price=random.uniform(100.0, 2000.0),
                url=f"http://example.com/flight/FL{i:03d}",
                createdDateKST=datetime(2024, 7, 20).date()
            )
            cheapest_flight.save()

        # Dummy data for ArrCountToICN
        for airport_code in ["JFK", "LAX", "NRT"]:
            arr_count = ArrCountToICN(
                depAirport=airport_code,
                count=random.randint(1, 10)
            )
            arr_count.save()

        # Dummy data for Weather
        base_date = datetime(2024, 7, 20)
        for i in range(10):
            weather = Weather(
                tmKST=(base_date + timedelta(days=i)).date(),
                avgTa=random.uniform(20.0, 30.0),
                minTa=random.uniform(15.0, 25.0),
                maxTa=random.uniform(25.0, 35.0),
                sumRn=random.uniform(0.0, 100.0)
            )
            weather.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))