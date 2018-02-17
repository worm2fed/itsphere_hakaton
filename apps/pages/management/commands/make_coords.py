# coding:utf-8
from django.core.management.base import BaseCommand
from apps.pages.models import Page
import googlemaps
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    def handle(self, *args, **options):
        pages = Page.objects.filter(position_text__isnull=False, position__isnull=True).exclude(position_text='')
        gmaps = googlemaps.Client(key='AIzaSyBUggg4I6FWB6sHijJGpXvBDdoZKqi1J7Y')
        for p in pages:
            print(p.id, p.position_text)
            print('@%s/%s' % (p.author, p.permlink))
            geocode_result = gmaps.geocode(p.position_text)
            if geocode_result.__len__() > 0:
                coords = geocode_result[0]['geometry']['location']
                p.position = Point(coords['lat'], coords['lng'])
                p.save()
