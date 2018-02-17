# coding:utf-8
from django.core.management.base import BaseCommand
from apps.pages.models import Page
import requests
import json

"""
Этот модуль обновляет стоимость страниц в зависимости от цены на золото
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        result = requests.get('http://data-asg.goldprice.org/GetData/RUB-XAU/1').text
        result = float(json.loads(result)[0].replace('RUB-XAU,',''))
        gold_price = result / 31.1034768

        def get_actual_price(gbg_price):
            return float('%.2f' % (gbg_price * gold_price / 1000.00))

        for page in Page.objects.filter(total_payout_value__isnull=False):
            gbg_price = float(page.total_payout_value.replace(' GBG', ''))
            Page.objects.filter(pk=page.id).update(actual_price=get_actual_price(gbg_price))

        for page in Page.objects.filter(total_payout_value__isnull=True,
                                        total_pending_payout_value__isnull=False):
            gbg_price = float(page.total_pending_payout_value.replace(' GBG', ''))
            Page.objects.filter(pk=page.id).update(actual_price=get_actual_price(gbg_price))
