import json
from datetime import datetime

from mptt.models import MPTTModel, TreeForeignKey
from bs4 import BeautifulSoup
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from django.utils.text import slugify
from transliterate import translit

from apps.auth_api.models import BlockChain, User

STATUS_CHOICES = (
    (0, u'Ошибка публикации'),
    (1, u'Публикуется'),
    (2, u'Опубликовано')
)

LOCALE_CHOICES = (
    ('ru', 'Русский'),
    ('en', 'English')
)

class MasterTag(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'Тэг дерева',
                            db_index=True)
    name = models.CharField(max_length=100, unique=False)
    description = models.CharField(max_length=1024, default='', unique=False)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Image(models.Model):
    file = models.ImageField()


class Page(models.Model):
    title = models.CharField(max_length=1000)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, related_name='pages')

    permlink = models.SlugField(unique=True, null=True, max_length=255)
    parent_permlink = models.CharField(max_length=1000, blank=True, null=True) # для статьи это категория
    body = models.TextField()

    total_payout_value = models.CharField(max_length=200, blank=True, null=True)
    total_pending_payout_value = models.CharField(max_length=200, blank=True, null=True)
    actual_price = models.FloatField(blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True)
    master_tag = models.ForeignKey(MasterTag, null=True)

    links = models.CharField(max_length=100000, blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True)
    miniature = models.ImageField(upload_to='thumbs', null=True, blank=True, max_length=500)

    voters = models.ManyToManyField(User, related_name='pages_vote', blank=True)

    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    locale = models.CharField(max_length=100, choices=LOCALE_CHOICES, default=LOCALE_CHOICES[0][0])



    def __str__(self):
        return str(self.title)

    class Meta:
        app_label = 'pages'

    def save(self, *args, **kwargs):
        if not self.permlink:
            num = 1
            slug = slugify(translit(self.title, 'ru', reversed=True))
            slug_uniq = slug

            while Page.objects.filter(permlink=slug_uniq).exists():
                slug_uniq = '{}-{}'.format(slug, num)
                num += 1

            self.permlink = slug_uniq

        super().save()

    def get_position(self):

        return {}

    def get_tags(self):
        return [t.name for t in self.tags.all()]

    def get_voters(self):
        return [p.user.username for p in self.voters.all()]

    def get_links(self):
        if self.links != '':
            return json.loads(self.links)
        return self.links

    def get_image(self):
        if self.images and self.images != '':
            r = json.loads(self.images.replace("'", "\""))
            if len(r) > 0:
                return r[0]
        return ''

    def miniature_link(self):
        if self.miniature:
            return self.miniature.url
        return '/static/dist/logo.png'


@receiver(pre_save, sender=Page)
def parse_links_and_img(sender, instance, **kwargs):
    page = instance
    soap = BeautifulSoup(page.body, 'html.parser')
    images_soap = soap.find_all('img')
    links_soap = soap.find_all('a')
    images = []
    for i in images_soap:
        images.append(i.get('src'))
    links = []
    for link in links_soap:
        links.append(link.get('href'))
    # page.images = json.dumps(images) if len(images)>0 else ''
    page.links = json.dumps(links) if len(links)>0 else ''


# !todo в течении суток обновлять голоса у страницы
#@receiver(pre_save, sender=Page)
#def check_new_votes(sender, instance, **kwargs):
#    old_instance = instance
#    if old_instance.voters.count() != instance.voters.count():
#        from steem import Steem
#        steem = Steem('wss://ws.mapala.net')
#        steem.vote()


class Comment(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    page = models.ForeignKey(Page, related_name='comments')
    permlink = models.CharField(max_length=512, null=True, blank=True)
    author = models.ForeignKey(User)
    voters = models.ManyToManyField(User, related_name='voters', blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)
    body = models.TextField(null=True)

    def __str__(self):
        return '%s - %s' % (self.author, self.body)

    def get_voters(self):
        return [p.user.username for p in self.voters.all()] if self.voters else []


@receiver(pre_save, sender=Comment)
def permlink_generator(sender, instance, **kwargs):
    if not instance.permlink:
        comment = instance
        parent = comment.parent
        pre = ''
        while (parent):
            pre += 're-%s-' % parent.author.user.username
            parent = parent.parent
        instance.permlink = '%sre-%s-%s-%s' % (pre, comment.page.author.user.username,
                                               comment.page.permlink,
                                               datetime.now().strftime('%Y%m%dt%H%M%Sz'))

    # todo убрать костыль, добавить auto_now=True, auto_now_add=True
    if not instance.created_at:
        instance.created_at = timezone.make_aware(datetime.now(), timezone.get_current_timezone())
    if not instance.updated_at:
        instance.updated_at = timezone.make_aware(datetime.now(), timezone.get_current_timezone())


class Parser_settings(models.Model):
    blockchain = models.ForeignKey(BlockChain)
    last_proceeded_block = models.BigIntegerField(default=0)
