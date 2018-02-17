# coding:utf-8
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from apps.auth_api.models import BlockChain
from apps.pages.management.commands.fetch import aware_date, author_define, tag_define, aware_date_blockchain
from apps.pages.models import Page, Parser_settings, Comment
import requests
import json


GOLOS_URL = 'http://node.golos.ws'
STEEMIT_URL = 'http://35.184.45.201:8090'

PARSED_LIMIT = 1433000000

"""
Парсер для засовывания в крон, в фоновом режиме обирает актуальные данные
"""


def parse_golos(start_block, setting, url):
    i = start_block
    blocks_done = 0
    while (i < (start_block + PARSED_LIMIT)):
        # if i % 100 == 0:
        # # print('operating block:', i)
        data = '{"jsonrpc":"2.0","id":"%s","method":"get_block","params": ["%d"]}' % (i, i)
        r = requests.get(url, data=data)
        rdict = json.loads(r.text)
        # # print(rdict)
        if not rdict['result']:
            if settings.DEBUG:
                print('end chain?')
            break
        for transaction in rdict['result']['transactions']:
            if (transaction['operations'][0][0] == "comment"):
                parent_author = transaction['operations'][0][1]['parent_author']
                parent_permlink = transaction['operations'][0][1]['parent_permlink']
                if parent_author == '':
                    permlink = transaction['operations'][0][1]['permlink']
                    author = transaction['operations'][0][1]['author']

                    data = '{"jsonrpc":"2.0","id":"%s","method":"get_content","params": ["%s\", "%s"]}' % (i, author, permlink)
                    r = requests.get(url, data=data)
                    article = json.loads(r.text)['result']

                    if parent_permlink != 'mapala':
                        # # print('NOT mapala')
                        # # print(json.loads(article.get('json_metadata'))['tags'])
                        continue

                    # >>>>>>>>>>>>>>>>>>>>>
                    print_article = json.loads(r.text)['result']
                    print_article['body'] = print_article['body'][:50]
                    print_article['active_votes'] = len(print_article['active_votes'])
                    print_article['json_metadata'] = json.loads(print_article.get('json_metadata'))
                    if 'image' in print_article['json_metadata']:
                        print_article['json_metadata']['image'] = len(print_article['json_metadata']['image'])
                    if 'links' in print_article['json_metadata']:
                        print_article['json_metadata']['links'] = len(print_article['json_metadata']['links'])
                    if settings.DEBUG:
                        print()
                        print("__PAGE in block %s," % i)
                        print(transaction['operations'][0][1]['parent_permlink'])
                        print('parent permlink', parent_permlink)
                        print('@%s/%s' % (author, permlink))
                        print('created: %s, updated: %s' % (print_article['created'],
                                                            print_article['last_update']))
                        print(print_article)
                    # <<<<<<<<<<<<<<<<<<<<

                    author = author_define(author, True)
                    p = Page.objects.get_or_create(author=author, permlink=permlink)
                    created = p[1]
                    p = p[0]
                    meta = json.loads(article.get('json_metadata'))

                    voters = [x['voter'] for x in article['active_votes']]
                    p.voters.clear()
                    for v in voters:
                        p.voters.add(author_define(v, True))

                    if created or p.updated_at < aware_date(article.get('last_update')):
                        p.title = article.get('title')
                        p.body = article.get('body')
                        p.status = 2
                        p.total_payout_value = article.get('total_payout_value')
                        p.total_pending_payout_value = article.get('total_pending_payout_value')
                        for meta_data in meta:
                            if meta_data == 'tags':
                                try:
                                    tags = [tag.lower() for tag in meta['tags']]
                                except:
                                    tags = None
                                if tags:
                                    for tag in tags:
                                        p.tags.add(tag_define(tag))
                            elif meta_data == 'image':
                                p.images = meta['image']
                            elif meta_data == 'links':
                                p.links = meta['links']
                            elif meta_data == 'location':
                                p.position_text = meta['location']
                            elif meta_data == 'coordinates':
                                coordinates = meta['location'].split(',')
                                try:
                                    position = Point(coordinates[0],
                                                                     coordinates[1])
                                except:
                                    position = None
                                p.position = position
                            elif meta_data in ['sign', 'users']:
                                pass
                            elif meta_data == 'app':
                                if meta['app'] not in ['mapala', 'steemit/0.1']:
                                    if settings.DEBUG:
                                        print('NEW_META', meta_data, meta[meta_data])
                            elif meta_data == 'model':
                                if meta['model'] not in ['blog', 'blogs', 'places', 'news']:
                                    if settings.DEBUG:
                                        print('NEW_META', meta_data, meta[meta_data])
                            elif meta_data == 'format':
                                if meta['format'] not in ['markdown']:
                                    if settings.DEBUG:
                                        print('NEW_META', meta_data, meta[meta_data])
                            else:
                                if settings.DEBUG:
                                    print('NEW_META', meta_data, meta[meta_data])
                        # category
                        p.tags.add(tag_define(parent_permlink))
                        p.save()
                        if settings.DEBUG:
                            print('page updated')

                    if article.get('children') > 0 and article.get('children') != p.comments.all().count():
                        pass
                        ## print('it must have %s children(s), now - %s' % (article.get('children'),
                        #                                                  p.comments.all().count()))
                        #
                        # data = '{"jsonrpc":"2.0","id":"%s","method":"get_content","params": ["parent_permlink\", "%s"]}' % (i, author, permlink)
                        # data = '{"jsonrpc":"2.0","id":"%s","method":"get_content","params": ["parent_permlink\", "%s"]}' % ( i, author, permlink)
                        # {"id": 12, "method": "get_content_replies",
                        # "params": ["golos", "cmo-or-weekly-analytical-report-or-2017-03-06"]}
                else:
                    pages = Page.objects.filter(author__user__username=parent_author, permlink=parent_permlink)
                    comments = Comment.objects.filter(author__user__username=parent_author, permlink=parent_permlink)
                    if not pages.exists() and not comments.exists():
                        continue
                    if settings.DEBUG:
                        print()
                        print('__COMMENT in block', i)
                        print(parent_author, parent_permlink)
                        print(transaction['operations'][0])
                    author = transaction['operations'][0][1]['author']
                    body = transaction['operations'][0][1]['body']
                    permlink = transaction['operations'][0][1]['permlink']
                    try:
                        created_at = aware_date_blockchain(permlink[-19:-4])
                    except ValueError:
                        # __COMMENT in block 4083088
                        # rodham
                        # smotrovaya - ploshadka - muzeya - murarium - zelenogradsk - sverkhu
                        # можно проверить дату создания в каком-то другом месте?
                        created_at = None
                    if pages.exists():
                        page = pages[0]
                        new_comment = Comment.objects.get_or_create(page=page, author=author_define(author, True),
                                                                    status=2, permlink=permlink)[0]
                        if not created_at:
                            created_at = page.created_at
                    elif comments.exists():
                        comment = comments[0]
                        new_comment = Comment.objects.get_or_create(parent=comment, page=comment.page,
                                                                    author=author_define(author, True),
                                                                    status=2, permlink=permlink)[0]
                        if not created_at:
                            created_at = comment.created_at

                    new_comment.body = body
                    new_comment.created_at = created_at
                    new_comment.save()
        i += 1
        blocks_done += 1
        setting.last_proceeded_block = start_block + blocks_done
        setting.save()
    # except Exception as exc:
    #        # print ('error , ', exc)
    #        pass
    # x['result']['transactions'][3]['operations'][0][0]
    return blocks_done


class Command(BaseCommand):
    help = ' Parse blocks from blockchain. Usage: ./manage.py parser <<golos or steem>> (default = golos)'

    def add_arguments(self, parser):
        parser.add_argument('command', nargs='+', type=str)
        pass

    def handle(self, *args, **options):
        cmd = options.get('command')

        if cmd[0] == 'steem':
            blockchain = BlockChain.objects.get(locale='en')
            if Parser_settings.objects.filter(blockchain=blockchain).count() == 0:
                Parser_settings(last_proceeded_block=10600000, blockchain=blockchain).save()
            setting = Parser_settings.objects.get(blockchain=blockchain)
            url = STEEMIT_URL
        else:
            blockchain = BlockChain.objects.get(locale='ru')
            if Parser_settings.objects.filter(blockchain=blockchain).count() == 0:
                Parser_settings(last_proceeded_block=4300000, blockchain=blockchain).save()
            setting = Parser_settings.objects.get(blockchain=blockchain)
            url = GOLOS_URL

        start_block = setting.last_proceeded_block
        if settings.DEBUG:
            print('start from', start_block)
        try:
            parse_golos(start_block, setting, url)
        except KeyboardInterrupt:
            pass
        except ConnectionError:
            pass
        blocks_done = setting.last_proceeded_block - start_block
        self.stdout.write(
            self.style.SUCCESS('parse %s blocks' % blocks_done)
        )
