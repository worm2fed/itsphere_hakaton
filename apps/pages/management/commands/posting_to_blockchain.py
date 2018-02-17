# coding:utf-8
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.pages.models import Page, Comment, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        pages = Page.objects.filter()

        comments = Comment.objects.filter(status=1)

        meta = {'app': 'mapala'}  # todo add url
        from steem import Steem
        for page in pages:
            steem = Steem(nodes=['wss://ws.golos.io'])
            steem.wallet.setKeys('5HrShnaADgYnWyMpyzJX5r75byBUVZUyqTRsBWmiNYjEYUGDBZT')
            mapala_tag = Tag.objects.get_or_create(name='mapala')[0]
            if mapala_tag not in page.tags.all():
                page.tags.add(mapala_tag)
            try:
                if settings.POST_TO_BLOCKCHAIN:

                    steem.post(
                      page.title,
                      page.body,
                      'b14ckb0x',
                      page.permlink, meta,
                      #category="test",
                      # tags=page.get_tags()
                    )
                page.status = 2
                print ('YOBO')
            except:
                page.status = 0
            page.save()

        for comment in comments:
            page = comment.page
            from steem import Steem
            steem = Steem(page.locale.master_node)
            steem.wallet.setKeys(comment.author.private_key)
            parent = comment.parent if comment.parent else page
            try:
                if settings.POST_TO_BLOCKCHAIN:
                    steem.post(
                        title='RE: %s' % page.title,
                        body=comment.body,
                        author=comment.author.user.username,
                        permlink=comment.permlink, meta=meta,
                        reply_identifier='@%s/%s' % (parent.author, parent.permlink))
                comment.status = 2
            except:
                comment.status = 0
            comment.save()
