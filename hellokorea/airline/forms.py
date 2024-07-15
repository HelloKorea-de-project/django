from django import forms

class FlightSearchForm(forms.Form):
    departure_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    arrival_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))