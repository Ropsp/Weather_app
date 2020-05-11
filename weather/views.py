from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
# Hakee säätiedot openweathermap API:sta
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=99a961b00bec40b2d1fed3bfeac9d9bf'
    
    error_message = ''
    message = ''
    message_class = '' 
# Tallentaa tekstikenttään annetun kaupungin.
# ja palauttaa ruudun annetun kaupungin kanssa.
    if request.method == 'POST':
        form = CityForm(request.POST)
# varmistaa että lisätty kaupunki on oikea kaupunki
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = City.objects.filter(name = new_city).count()
# Jos syötettyä kaupunkia ei löydy. Tieto tallentuu kantaan. 
# Tai tulee virheilmoitus.           
            if existing_city == 0:
                response = requests.get(url.format(new_city)).json()
# Tarkistaa onko syötettyä kaupunkia olemassa.                
                if response['cod'] == 200:
                    form.save()
                else:
                    error_message = 'This city does not exist.'
            else:
               error_message = 'City already exists.' 
# Tarkistaa millainen viesti lähetetään.
        if error_message:
            message = error_message
            message_class = 'is-danger'
        else:
            message = 'City added.'
            message_class = 'is-success'
    form = CityForm()  

    cities = City.objects.all()
# Lista johon säätiedot laitetaan
    weather_data = []
# Käy läpi kannassa olevat kaupungit ja asettaa jokaiselle oikeat attribuutit.
    for city in cities:

        response = requests.get(url.format(city)).json()
    # Hakee halutut tiedot json responsesta.
    # Eli kaupunki, lämpötila, kuvaus ja sääkuvake.
    # Lisää kaupungin listaan.
        city_weather = {
            'city' : city.name,
            'temperature' : response['main']['temp'],
            'description' : response['weather'][0]['description'],
            'icon' : response['weather'][0]['icon'],
        }    
        weather_data.append(city_weather)
# Välittää tiedon weather.html sivulle.    
    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }
    return render(request, 'weather/weather.html', context)
# Metodi kaupungin poistamiseksi
def delete_city(request, city_name):
    City.objects.get(name = city_name).delete()
    return redirect('main')