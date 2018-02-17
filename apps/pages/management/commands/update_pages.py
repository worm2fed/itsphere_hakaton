# coding:utf-8
from datetime import timedelta
from django.core.management.base import BaseCommand
from apps.pages.management.commands.fetch import aware_date, author_define
from apps.pages.models import Page
import requests
import json
from django.utils.timezone import datetime


BLOCKCHAIN_URL = 'wss://ws.mapala.net'

"""
Этот модуль обновляет данные страниц в течении суток после их добавления
"""


class Command(BaseCommand):
  def handle(self, *args, **options):
    pages = Page.objects.filter(created_at__gte=datetime.now() - timedelta(days=1))
    for page in pages:
        author = page.author.user.username
        permlink = page.permlink
        data = '{"jsonrpc":"2.0","id":"25","method":"get_content","params": ["%s\", "%s"]}' % (author, permlink)
        r = requests.get(BLOCKCHAIN_URL, data=data)
        article = json.loads(r.text)['result']
        page.total_payout_value = article.get('total_payout_value'),
        page.total_pending_payout_value = article.get('total_pending_payout_value')
        voters = json.loads(article.get('voters'))
        for v in voters:
            page.voters.add(author_define(v, True).id)
        page.body = article.get('body')
        page.title = article.get('title')
        page.updated_at = aware_date(article.get('last_update'))
        page.save()

    self.stdout.write(
      self.style.SUCCESS('updated %s pages' % pages.count())
    )
