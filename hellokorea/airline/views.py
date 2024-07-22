# from django.shortcuts import render
# from .models import Flight
# from .forms import FlightSearchForm

# def index(request):
#     form = FlightSearchForm()
#     flights = None

#     if request.method == 'GET':
#         form = FlightSearchForm(request.GET)
#         if form.is_valid():
#             departure_date = form.cleaned_data['departure_date']
#             arrival_date = form.cleaned_data['arrival_date']
#             flights = Flight.objects.filter(departure_date=departure_date, arrival_date=arrival_date)
    
#     return render(request, 'airline/index.html', {'form': form, 'flights': flights})


from django.shortcuts import render
from django.http import JsonResponse
from .models import AirportInformation, ExchangeRate, CheapestFlight, Weather
from datetime import datetime, timedelta
from pytz import timezone, all_timezones
# from timezonefinder import TimezoneFinder
# from countryinfo import CountryInfo

def index(request):
    # Get all airports for the dropdown
    airports = AirportInformation.objects.all()

    today = datetime.today().date()
    one_month_later = today + timedelta(days=30)
    one_week_later = today + timedelta(days=7)

    # Fetch flights within the next month
    flights = CheapestFlight.objects.filter(arrTimeUTC__date__range=[today, one_month_later])

    # Fetch weather data for the next week
    weather_data = Weather.objects.filter(tmKST__range=[today, one_week_later])

    context = {
        'airports': airports,
        'flights': flights,
        'weather_data': weather_data,
    }

    return render(request, 'airline/index.html', context)

def search_flights(request):
    dep_airport = request.GET.get('options')
    dep_date = request.GET.get('depDate')
    arr_date = request.GET.get('arrDate')

    # Get all airports for the dropdown
    airports = AirportInformation.objects.all()

    # Get departure airport information
    airport_info = AirportInformation.objects.get(airportCode=dep_airport)
    # dep_country_time_zone = timezone(airport_info.countryName)
    kst_time_zone = timezone('Asia/Seoul')

    # Convert dep_date to UTC
    dep_date_obj = datetime.strptime(dep_date, '%Y-%m-%d')
    # dep_date_local = dep_country_time_zone.localize(datetime.combine(dep_date_obj, datetime.min.time()))
    dep_date_utc = dep_date_obj.astimezone(timezone('UTC')) 

    # Convert arr_date to KST then to UTC
    arr_date_obj = datetime.strptime(arr_date, '%Y-%m-%d')
    arr_date_kst = kst_time_zone.localize(datetime.combine(arr_date_obj, datetime.min.time()))
    arr_date_utc = arr_date_kst.astimezone(timezone('UTC'))

    # Fetch flights based on search criteria
    flights = CheapestFlight.objects.filter(depAirport=dep_airport, depTimeUTC__date=dep_date_utc.date(), arrTimeUTC__date=arr_date_utc.date())
    flights = CheapestFlight.objects.filter(depTimeUTC__date=dep_date_obj.date())


    # Fetch exchange rate for the departure airport's country
    exchange_rate = ExchangeRate.objects.filter(currency=airport_info.currency).first()

    # Fetch weather data for the arrival date and the following week
    weather_data = Weather.objects.filter(tmKST__range=[arr_date_obj, arr_date_obj + timedelta(days=7)])

    context = {
        'airports': airports,
        'flights': flights,
        'exchange_rate': exchange_rate,
        'weather_data': weather_data,
    }


    return render(request, 'airline/index.html', context)

# def get_timezone_by_country(country_name):
#     try:
#         country = CountryInfo(country_name)
#         lat, lon = country.info()['latlng']
#         tf = TimezoneFinder()
#         tz_name = tf.timezone_at(lat=lat, lng=lon)
        
#         if tz_name in all_timezones:
#             return timezone(tz_name)
#         else:
#             raise ValueError(f"Time zone for country '{country_name}' not found.")
#     except KeyError:
#         raise ValueError(f"Information for country '{country_name}' not found.")