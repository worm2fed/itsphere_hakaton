# coding:utf-8
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from apps.pages.models import Page, Tag, MasterTag, Comment
import requests
import json
from django.utils.timezone import datetime
from django.utils import timezone
from backend.settings import STATIC_ROOT

from apps.auth_api.models import User

MAPALA_URL = 'http://mapala.net/api/v1/site/'


"""
Этот модуль запрашивает с mapala.net данные и набивает базу проекта
"""


def aware_date(date):
    adate = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    return timezone.make_aware(adate, timezone.get_current_timezone())


def aware_date_mapala(date):
    adate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return timezone.make_aware(adate, timezone.get_current_timezone())


def aware_date_blockchain(date):
    adate = datetime.strptime(date, '%Y%m%dt%H%M%S')
    return timezone.make_aware(adate, timezone.get_current_timezone())


MASTER_TAGS = {'Знания': [
                        'Лайфхак',
                        'Традиции',
                        'Разное', ],
               'Места': [
                        'Природа',
                        'Человек', ],
               'Блоги': [
                        'Приключения', ],
               'Сообщество': [
                        'Предложение',
                        'Отзыв',
                        'Руководство',
                        'Хочу в команду',
                        'Конкурс',
                        'Купол',
                        'Иммиграция', ],
               'Новости':[
                        'Блог',
                        'Сайт',
                        'ICO',
                        'Команда',],}

# todo возможность написать свой мастертэг
def mapala_tags(BLOCKCHAIN):
    # забираем все тэги из альфа (yii)
    url = MAPALA_URL + 'get_tree?blockchain=%s' % BLOCKCHAIN
    r = requests.get(url)
    rdict = json.loads(r.text)
    for tag in rdict:
        Tag.objects.get_or_create(name=tag['text'])

    # подчищаем master-тэги, оставляя только нашу новую структуру
    MasterTag.objects.all().delete()
    for tag in MASTER_TAGS:
        mastertag_define(tag)
        for sub_tag in MASTER_TAGS[tag]:
            mastertag_define(tag, sub_tag)
    return True


def author_define(name, force_add=False):
    if force_add:
        user = User.objects.get_or_create(username=name)[0]
    else:
        user = User.objects.filter(username=name)

    return user


def from_up_lowers(s):
    if type(s) == str:
        return s[0].upper() + s[1:].lower()
    return s


def mastertag_define(name, child=None):
    if name == '[]':
        return False
    tag = MasterTag.objects.get_or_create(name=from_up_lowers(name))[0]

    if child:
        if child in ['[]', 'Вне', 'Унсортед', 'Вне_города']:
            return False
        child = MasterTag.objects.get_or_create(name=from_up_lowers(child))[0]
        if child != tag:
            if not child.parent and child.name not in MASTER_TAGS:
                child.parent = tag
                child.save()
            return child
    return tag


def tag_define(name):
    return Tag.objects.get_or_create(name=name)[0]


def mapala_pages(BLOCKCHAIN):
    url = MAPALA_URL + 'index?blockchain=%s' % BLOCKCHAIN

    # запрашивает с мапалы только отсутствующие в базе страницы
    data = requests.get(url).json()

    for article in data['allModels']:
        if any(key not in article for key in ['title', 'author', 'body']):
            continue

        try:
            author = author_define(article.get('author'), True)
            article['meta'] = json.loads(article['meta'])

            try:
                tags = [tag.lower() for tag in article.get('meta').get('tags')]
            except:
                tags = None

            position = None

            if 'coordinates' in article['meta'] and article['meta']['coordinates'] != '':
                try:
                    position = Point(article['meta']['coordinates'].split(',')[0],
                                     article['meta']['coordinates'].split(',')[1])
                except:
                    position = None

            position_text = ''

            if 'location' in article['meta']:
                position_text = article['meta']['location']
            if Page.objects.filter(author=author, permlink=article.get('permlink')).exists():
                continue
            else:
                page = Page(author_id=author.id,
                            title=article.get('title'),
                            permlink=article.get('permlink'))

            page.created_at = aware_date_mapala(article.get('created_at'))
            page.updated_at = aware_date_mapala(article.get('updated_at'))
            page.body = article.get('body')
            page.image = article.get('meta').get('image')
            page.parent_permlink = article.get('parent_permlink')


            if BLOCKCHAIN == 'golos':
                page.locale = 'ru'
            else:
                page.locale = 'en'

            page.total_payout_value = article.get('total_payout_value')
            page.total_pending_payout_value = article.get('total_pending_payout_value')
            page.status = 2
            page.position = position
            page.position_text = position_text
            page.save()

            if tags:
                for tag in tags:
                    page.tags.add(tag_define(tag))

            voters = json.loads(article.get('voters'))

            for v in voters:
                page.voters.add(author_define(v, True).id)

            country = article.get('country')
            city = article.get('city')
            category = article.get('category')
            sub_category = article.get('sub_category')

            for m_t in [mastertag_define('mapala_places', country),
                        mastertag_define(country, city),
                        mastertag_define('mapala_categories', category),
                        mastertag_define(category, sub_category)]:
                if m_t:
                    page.master_tag = m_t

            page.save()
            get_comments_for(page, page.permlink)
        except Exception as e:
            print('Warning: ', e)

    return True


def get_comments_for(page, permlink, parent_comment=None):
    url = MAPALA_URL + 'get_comment?parent_permlink=%s' % permlink
    r = requests.get(url)
    rdict = json.loads(r.text)
    for comment in rdict:
        """
        [{"id": "5978",
          "updated_at": "2017-03-02 08:32:51",
          "created_at": "2017-03-02 08:32:51",
          "country": null,
          "city": null,
          "category": null,
          "sub_category": null,
          "votes": "0",
          "author": "polyideic",
          "title": "",
          "total_pending_payout_value": "0",
          "replies": "0",
          "body": "Да, в ленте видно!\nМожно. Но получится, что Вы второй раз опубликуете их и на голосе",
          "meta": "{\"tags\":[\"mapala\"]}",
          "blockchain": "golos",
          "voters": "[]",
          "permlink": "re-anela-re-polyideic-rukovodstvo-kak-snova-razmeshchatx-posty-na-mapalanet-20170302t083245812z",
          "currency": "GBG",
          "parent_permlink": "re-polyideic-rukovodstvo-kak-snova-razmeshchatx-posty-na-mapalanet-20170302t082836744z",
          "entity": "2520b329",
          "relatedTo": "common\\models\\Art:rukovodstvo-kak-snova-razmeshchatx-posty-na-mapalanet",
          "status": "1",
          "level": "1"}]
        """
        author = author_define(comment.get('author'), True)
        c = Comment.objects.get_or_create(page=page, author=author, body=comment.get('body'),
                                          permlink=comment.get('permlink'),status = 2,
                                            parent=parent_comment if parent_comment else None)[0]
        c.created_at = aware_date_mapala(comment.get('created_at'))
        c.updated_at = aware_date_mapala(comment.get('updated_at'))
        c.save()
        if comment.get('voters') != '[]':
            print(comment.get('voters'))

        get_comments_for(page, comment.get('permlink'), c)
    return True


def mapala_users():
    import csv

    with open('./apps/pages/management/commands/users_dump.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for r in reader:
            username = r[1]
            email = r[7]

            if len(username.strip()) < 1:
                continue

            if User.objects.filter(username=username).exists():
                continue

            if User.objects.filter(email=email).exists():
                email = None

            user = {
                'username': username,
                'password': 'bcrypt_sha256$%s' % r[4],
            }

            if not User.objects.filter(email=email).exists():
                user['email'] = r[7]

            User.objects.create(**user)


class Command(BaseCommand):
    help = ' Fetch from alpha mapala. Usage: ./manage.py fetch <<golos or steem>> (default = golos)'

    def add_arguments(self, parser):
        parser.add_argument('command', nargs='+', type=str)

    def handle(self, *args, **options):
        cmd = options.get('command')

        blockchain = cmd[0]

        mapala_tags(blockchain)
        if settings.DEBUG:
            print('Tags:', Tag.objects.all().count())
            print('Mastertags:', MasterTag.objects.all().count())

        mapala_users()
        if settings.DEBUG:
            print('Users:', User.objects.all().count())

        Comment.objects.filter(permlink__isnull=True).delete()

        mapala_pages(blockchain)
        if settings.DEBUG:
            print('Pages:', Page.objects.all().count())
            print('Comments:', Comment.objects.all().count())

        self.stdout.write(
            self.style.SUCCESS('Fetch done')
        )
