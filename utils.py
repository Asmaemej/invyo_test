"""
Module that declares static utility functions
"""
import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import json


def list_to_json_file(l, filename):
    """
    Sorry, don't have time to comment all functions :(
    """
    with open(filename, "w") as f:
        json.dump(l, f)


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


def geocode_from_api(address):
    url = 'http://api-adresse.data.gouv.fr/search/'
    response = requests.get(url, params={'q': address, 'limit': 1})
    geocode_json = response.json()
    longitude = geocode_json['features'][0]['geometry']['coordinates'][0]
    latitude = geocode_json['features'][0]['geometry']['coordinates'][1]
    return latitude, longitude


def geocode_from_geopy(address):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(address)
    return location.latitude, location.longitude


def get_lat_long(address):
    if 'France' in address:
        latitude, longitude = geocode_from_api(address)
    else:
        latitude, longitude = geocode_from_geopy(address)
    return latitude, longitude


def add_lat_long(l):
    companies_list = []
    companies_without_address = []
    for item in l:
        try:
            lat, long = get_lat_long(item['address'] + " " + item['city_id'] + " " + item['country_id'])
            if lat is not None and long is not None:
                companies_list.append({'company_id': item['company_id'],
                                       'latitude': lat,
                                       'longitude': long
                                       })
        except:
            companies_without_address.append(item['company_id'])
    return companies_list


def calcul_distance(entrepot, company):
    distance = geodesic(entrepot, company).km
    if distance < 20:
        class_n = 1
    elif 20 <= distance < 100:
        class_n = 2
    else:
        class_n = 3
    return class_n
