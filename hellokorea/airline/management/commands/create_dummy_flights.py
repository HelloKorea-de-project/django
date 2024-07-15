# import random
# from datetime import timedelta
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from faker import Faker
# from airline.models import Flight

# class Command(BaseCommand):
#     help = 'Create dummy flight data'

#     def handle(self, *args, **kwargs):
#         fake = Faker()
#         Flight.objects.all().delete()

#         cities = ['Seoul', 'Tokyo', 'New York', 'Los Angeles', 'Paris', 'London', 'Berlin', 'Moscow', 'Sydney', 'Dubai']

#         for _ in range(50):
#             departure_city = random.choice(cities)
#             arrival_city = random.choice([city for city in cities if city != departure_city])
#             departure_date = fake.date_between(start_date='-1y', end_date='today')
#             arrival_date = departure_date + timedelta(days=random.randint(1, 10))

#             Flight.objects.create(
#                 flight_number=fake.unique.numerify('FL###'),
#                 departure_city=departure_city,
#                 arrival_city=arrival_city,
#                 departure_date=departure_date,
#                 arrival_date=arrival_date
#             )

#         self.stdout.write(self.style.SUCCESS('Successfully created dummy flight data'))

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from airline.models import Flight

class Command(BaseCommand):
    help = 'Create dummy flight data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        Flight.objects.all().delete()

        cities = ['Seoul', 'Tokyo', 'New York', 'Los Angeles', 'Paris', 'London', 'Berlin', 'Moscow', 'Sydney', 'Dubai']

        for _ in range(50):
            departure_city = random.choice(cities)
            arrival_city = random.choice([city for city in cities if city != departure_city])
            departure_date = fake.date_between(start_date='today', end_date='+30d')
            arrival_date = departure_date + timedelta(days=random.randint(1, 10))

            Flight.objects.create(
                flight_number=fake.unique.numerify('FL###'),
                departure_city=departure_city,
                arrival_city=arrival_city,
                departure_date=departure_date,
                arrival_date=arrival_date
            )

        self.stdout.write(self.style.SUCCESS('Successfully created dummy flight data'))
