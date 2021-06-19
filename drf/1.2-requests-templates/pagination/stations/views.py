import csv
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    class Station:
        def __init__(self, Name, Street, District):
            self.Name = Name
            self.Street = Street
            self.District = District

    stations_list = []
    with open(settings.BUS_STATION_CSV, encoding='utf-8') as stations_data:
        stations = csv.DictReader(stations_data)
        for station in stations:
            stations_list.append(
                Station(
                    station.get('Name'),
                    station.get('Street'),
                    station.get('District')
                )
            )

    paginator = Paginator(stations_list, 10)
    current_page = request.GET.get('page', 1)
    page = paginator.get_page(current_page)
    context = {
         'bus_stations': page.object_list,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
