# coding:utf-8
import piston
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):

        from steem import Steem
        steem = Steem('wss://ws.mapala.net')

        steem.wallet.setKeys('5HyrRSrm4taTzH5gubLxrnN3BT1tEfnWzzERKy9ohHxGVD6vzVq')

        steem.post("Testing steem library", "I am testing steem", author='sci', category="test")

        self.stdout.write(
            self.style.SUCCESS('done')
        )
