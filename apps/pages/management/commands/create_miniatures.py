# coding:utf-8
import random
import shutil
import string
from urllib.error import HTTPError, URLError
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models.functions.base import Length
from django.db.models.query_utils import Q
from apps.pages.models import Page
from PIL import Image
import json
import urllib.request

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def do_pages():
    pages = Page.objects.annotate(img_len=Length('images')).filter(img_len__gt=2). \
        filter(Q(miniature__isnull=True) | Q(miniature='')). \
        order_by('-id')
    count = pages.count()
    for page in pages:
        r = json.loads(page.images.replace("'", "\""))
        img_url = r[0].split('?')[0]
        rand_str = lambda n: ''.join([random.choice(string.ascii_lowercase + string.digits) for i in iter(range(n))])
        filename = '%s.jpg' % rand_str(8)  # r[0].split('/')[-1]
        # result = urllib.request.urlretrieve(img_url)

        if img_url.startswith('h3>'):
            img_url = img_url[3:]

        if settings.DEBUG:
            print(img_url)
        error = False
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            img = urllib.request.urlopen(req)  # .read()
            # img = urllib.request.urlopen(img_url)
        except HTTPError:
            if settings.DEBUG:
                print('http error')
            error = True
        except UnicodeEncodeError:
            if settings.DEBUG:
                print('unicode error')
            error = True
        except URLError:
            if settings.DEBUG:
                print('URL error')
            error = True
        # todo если ошибка, удалять эту картинку из массива картинок
        if error:
          Page.objects.filter(id=page.id).update(images=json.dumps(r[1:]) if r[1:].__len__() > 0 else None)
          continue

        full_path = '%sthumbs/%s' % (settings.MEDIA_ROOT, filename)
        with open(full_path, 'wb') as fhand:
          shutil.copyfileobj(img, fhand)

        size = 200, 150

        outfile = full_path  # os.path.splitext(full_path)[0] + ".thumbnail"
        try:
          im = Image.open(full_path)
          im.thumbnail(size, Image.ANTIALIAS)

          width, height = im.size  # Get dimensions

          # im.crop((0, 0, 200, 150)) todo!

          im.save(outfile, "JPEG")
        except IOError:
          if settings.DEBUG:
              print("cannot create thumbnail for")

        # # print(thumbnail.get_thumbnail(full_path, size, crop='center'))
        # page.miniature = thumbnail.get_thumbnail(full_path, size, crop='center')#'/thumbs/%s' % filename
        page.miniature = '/thumbs/%s' % filename
        page.save()
        if settings.DEBUG:
            print(page.id)
    return count


class Command(BaseCommand):
    def handle(self, *args, **options):
        done = do_pages()
        while (done > 0):
            if settings.DEBUG:
                print()
                print('done', done)
                print()
            done = do_pages()
