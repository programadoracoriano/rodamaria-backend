import os
import django
import requests
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Initialize Django
django.setup()
from django.conf import settings
from databank.models import PlaceCategory, Place

from django.core.management.base import BaseCommand
# Set the DJANGO_SETTINGS_MODULE environment variable



class Command(BaseCommand):
    def handle(self, *args, **options):
        val_input = input("Insere uma categoria: ")
        if val_input is not None:
            GET_CAT = PlaceCategory.objects.get(name=val_input)
            TYPES_TRANSLATION = {
                'hotel': 1,
                'restaurant': 3,
                'viewpoint': 4
                # Add more translations as needed
            }

            # Replace with your own API key
            API_KEY = 'AIzaSyA1mFLK9Omf1jic1fz8tJH0NL6I0FOipEE'

            # Place search endpoint
            SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
            PHOTO_URL = 'https://maps.googleapis.com/maps/api/place/photo'


            def get_places_in_zone(latitude, longitude, radius, keywords=None):
                """
                Get places within a specific zone defined by latitude, longitude, and radius.
                Optional: provide a keyword to filter the results.
                """
                params = {
                    'location': f'{latitude},{longitude}',
                    'radius': radius,
                    'key': API_KEY,
                    'language': 'pt'
                }
                if keywords:
                    keyword_str = '|'.join(keywords)
                    params['keyword'] = keyword_str

                response = requests.get(SEARCH_URL, params=params)
                data = response.json()
                return data
            def get_photo_url(photo_reference, max_width):
                """
                Get the photo URL for a given photo reference and maximum width.
                """
                params = {
                    'maxwidth': max_width,
                    'photoreference': photo_reference,
                    'key': API_KEY
                }
                response = requests.get(PHOTO_URL, params=params)
                if response.status_code == 200:
                    return response.url
                else:
                    return None

            def scrape_places_in_zone(latitude, longitude, radius, keyword=None):
                """
                Scrape and print information about places within a specific zone.
                Optional: provide a keyword to filter the results.
                """
                place_data = get_places_in_zone(latitude, longitude, radius, keyword)
                if place_data['status'] == 'OK':
                    results = place_data['results']
                    for place in results:
                        name = place.get('name', 'N/A')
                        address = place.get('vicinity', 'N/A')
                        rating = place.get('rating', 'N/A')
                        types = place.get('types', [])
                        coordinates = place.get('geometry', {}).get('location', {})
                        latitude = coordinates.get('lat', 'N/A')
                        longitude = coordinates.get('lng', 'N/A')
                        photos = place.get('photos', [])
                        photo_url = ''
                        print('Name:', name)
                        print('Address:', address)
                        print('Rating:', rating)
                        print('Types:', types)
                        print('Latitude:', latitude)
                        print('Longitude:', longitude)
                        print('Fotos:')

                        for photo in photos:
                            photo_reference = photo.get('photo_reference', '')
                            photo_width = photo.get('width', 400)
                            photo_url = get_photo_url(photo_reference, photo_width)
                            if photo_url:
                                print(photo_url)
                        print('-' * 20)
                        Place.objects.create(name=name, category=GET_CAT,
                                            api_image=photo_url,
                                            lat=latitude, lng=longitude)
                else:
                    print('Error:', place_data['status'])

            # Example usage
            latitude = 36.98117020558753  # Latitude of the center of the zone
            longitude = -25.103280712732392  # Longitude of the center of the zone
            radius = 10000  # Radius in meters
            keywords = [val_input]  # Optional keyword to filter results

            scrape_places_in_zone(latitude, longitude, radius, keywords)
        else:
            pass

Command.handle(self=None)
