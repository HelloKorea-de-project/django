from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from datetime import datetime, timedelta
from pytz import timezone, all_timezones
from django.utils.timezone import make_aware
from django.db.models import Q
from timezonefinder import TimezoneFinder
from countryinfo import CountryInfo

def index(request):
    # Get all airports for the dropdown
    airports = CheapestFlight.objects.values('depAirportCode').distinct()

    today = datetime.today().date()
    one_month_later = today + timedelta(days=30)
    one_week_later = today + timedelta(days=7)

    # Fetch flights within the next month
    flights = CheapestFlight.objects.filter(arrTime__date__range=[today, one_month_later])
    # Apply timezone conversion to arrTime field for each flight
    for flight in flights:
        try:
            dep_country_code = flight.depCountryCode
            flight_dep_timezone = get_timezone_by_country(dep_country_code)
            flight.depTime = flight.depTime.astimezone(flight_dep_timezone)
            flight.arrTime = flight.arrTime.astimezone(timezone('Asia/Seoul'))
        except Exception as e:
            print(f"Error converting timezone for flight {flight.id}: {e}")

    # Fetch weather data for the next week
    weather_data = Weather.objects.filter(tm__range=[today, one_week_later])

    context = {
        'airports': airports,
        'flights': flights,
        'weather_data': weather_data,
    }

    return render(request, 'airline/index.html', context)

def search_flights(request):
    dep_airport = request.GET.get('depAirportCodes')
    dep_date = request.GET.get('depDate')
    arr_date = request.GET.get('arrDate')

    # Get all airports for the dropdown
    airports = CheapestFlight.objects.values('depAirportCode').distinct()

    if not dep_airport:
        return render(request, 'airline/index.html', {'airports': airports, 'error': 'Departure airport must be selected.'})

    filters = {'depAirportCode': dep_airport}
    q_objects = Q(depAirportCode=dep_airport)

    if dep_date:
        dep_date_utc = get_tz_date(dep_date)
        q_objects &= Q(depTime__date=dep_date_utc.date())

    if arr_date:
        arr_date_utc = get_tz_date(arr_date, 'Asia/Seoul')
        q_objects &= Q(arrTime__date=arr_date_utc.date())

    flights = CheapestFlight.objects.filter(q_objects)
    # Apply timezone conversion to arrTime field for each flight
    for flight in flights:
        try:
            dep_country_code = flight.depCountryCode
            flight_dep_timezone = get_timezone_by_country(dep_country_code)
            flight.depTime = flight.depTime.astimezone(flight_dep_timezone)
            flight.arrTime = flight.arrTime.astimezone('Asia/Seoul')
        except Exception as e:
            print(f"Error converting timezone for flight {flight.id}: {e}")

    airport_info = CheapestFlight.objects.get(depAirportCode=dep_airport)
    exchange_rate = ExchangeRate.objects.filter(currencyCode=airport_info.currencyCode).first()

    weather_data_date = arr_date if arr_date else dep_date
    weather_data = None

    if weather_data_date:
        weather_data_date_obj = datetime.strptime(weather_data_date, '%Y-%m-%d')
        weather_data = Weather.objects.filter(tm__range=[weather_data_date_obj, weather_data_date_obj + timedelta(days=7)])

    context = {
        'airports': airports,
        'flights': flights,
        'exchange_rate': exchange_rate,
        'weather_data': weather_data,
    }

    return render(request, 'airline/index.html', context)

def get_tz_date(date_str, time_zone='UTC'):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_aware = make_aware(date_obj).astimezone(timezone(time_zone))
    return date_aware

def get_timezone_by_country(country_name):
    try:
        country = CountryInfo(country_name)
        lat, lon = country.info()['latlng']
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lat=lat, lng=lon)
        
        if tz_name in all_timezones:
            return timezone(tz_name)
        else:
            raise ValueError(f"Time zone for country '{country_name}' not found.")
    except KeyError:
        raise ValueError(f"Information for country '{country_name}' not found.")