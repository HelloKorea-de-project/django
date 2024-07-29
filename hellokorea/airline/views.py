from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from datetime import datetime, timedelta
from pytz import timezone, all_timezones
from django.utils.timezone import make_aware
from django.db.models import Q
from timezonefinder import TimezoneFinder
from countryinfo import CountryInfo
from django.core.paginator import Paginator, EmptyPage
from django.template.loader import render_to_string
import asyncio
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

async def index(request):
    # Get all airports for the dropdown
    airports = await sync_to_async(lambda: list(CheapestFlight.objects.values('depAirportCode').distinct()))()

    today = datetime.today().date()
    one_month_later = today + timedelta(days=30)

    one_year_ago = today - timedelta(days=366)
    one_year_ago_one_week = one_year_ago + timedelta(days=6)

    # Fetch flights within the next month
    flights = await sync_to_async(lambda: list(CheapestFlight.objects.filter(arrTime__date__range=[today, one_month_later])))()

    # Paginate flights
    paginator = Paginator(flights, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Apply timezone conversion to arrTime field for each flight
    tasks = [convert_timezones(flight) for flight in page_obj]
    page_obj = await asyncio.gather(*tasks)

    # Fetch weather data for the next week
    weather_data = await sync_to_async(lambda: list(Weather.objects.filter(tm__range=[one_year_ago, one_year_ago_one_week])))()

    context = {
        'airports': airports,
        'flights': page_obj,
        'weather_data': weather_data,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            return JsonResponse({
                'html': render_to_string('airline/flight_list.html', {'flights': page_obj})
            })
        except Exception as e:
            logger.error(f"Error rendering template: {e}")
            return JsonResponse({
                'error': 'Error rendering template'
            }, status=500)

    return render(request, 'airline/index.html', context)

async def search_flights(request):
    dep_airport = request.GET.get('depAirportCodes')
    dep_date = request.GET.get('depDate')
    arr_date = request.GET.get('arrDate')

    # Get all airports for the dropdown
    airports = await sync_to_async(lambda: list(CheapestFlight.objects.values('depAirportCode').distinct()))()

    if not dep_airport:
        return render(request, 'airline/index.html', {'airports': airports, 'error': 'Departure airport must be selected.'})

    q_objects = Q(depAirportCode=dep_airport)

    if dep_date:
        dep_date_utc = get_tz_date(dep_date)
        q_objects &= Q(depTime__date=dep_date_utc.date())

    if arr_date:
        arr_date_utc = get_tz_date(arr_date, 'Asia/Seoul')
        q_objects &= Q(arrTime__date=arr_date_utc.date())

    flights = await sync_to_async(lambda: list(CheapestFlight.objects.filter(q_objects)))()

    # Paginate flights
    paginator = Paginator(flights, 5)  # Show 10 flights per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Apply timezone conversion to arrTime field for each flight
    tasks = [convert_timezones(flight) for flight in page_obj]
    page_obj = await asyncio.gather(*tasks)

    exchange_rate = None
    if page_obj:
        # airport_info = await sync_to_async(lambda: CheapestFlight.objects.filter(depAirportCode=dep_airport).first())()
        exchange_rate = await sync_to_async(lambda: list(ExchangeRate.objects.get(currencyCode=page_obj[0].currencyCode)))()

    weather_data_date = arr_date if arr_date else dep_date
    weather_data = None

    if weather_data_date:
        weather_data_date_obj = datetime.strptime(weather_data_date, '%Y-%m-%d')
        one_year_ago = weather_data_date_obj - timedelta(days=366)
        one_year_ago_one_week = one_year_ago + timedelta(days=6)
        weather_data = await sync_to_async(lambda: list(Weather.objects.filter(tm__range=[one_year_ago, one_year_ago_one_week])))()

    context = {
        'airports': airports,
        'flights': page_obj,
        'exchange_rate': exchange_rate,
        'weather_data': weather_data,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            return JsonResponse({
                'html': render_to_string('airline/flight_list.html', {'flights': page_obj})
            })
        except Exception as e:
                logger.error(f"Error rendering template: {e}")
                return JsonResponse({
                    'error': 'Error rendering template'
                }, status=500)

    return render(request, 'airline/index.html', context)

async def convert_timezones(flight):
    try:
        dep_country_code = flight.depCountryCode
        flight_dep_timezone = await get_timezone_by_country(dep_country_code)
        flight.depTime = flight.depTime.astimezone(flight_dep_timezone)
        flight.arrTime = flight.arrTime.astimezone(timezone('Asia/Seoul'))
    except Exception as e:
        print(f"Error converting timezone for flight {flight.id}: {e}")
    return flight

def get_tz_date(date_str, time_zone='UTC'):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    date_aware = make_aware(date_obj).astimezone(timezone(time_zone))
    return date_aware

async def get_timezone_by_country(country_name):
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