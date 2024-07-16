from django.shortcuts import render
from .models import Flight
from .forms import FlightSearchForm

def index(request):
    form = FlightSearchForm()
    flights = None

    if request.method == 'GET':
        form = FlightSearchForm(request.GET)
        if form.is_valid():
            departure_date = form.cleaned_data['departure_date']
            arrival_date = form.cleaned_data['arrival_date']
            flights = Flight.objects.filter(departure_date=departure_date, arrival_date=arrival_date)
    
    return render(request, 'airline/index.html', {'form': form, 'flights': flights})
