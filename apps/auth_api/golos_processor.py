from django.core.management import BaseCommand
from steem import Steem

from apps.auth_api.models import Post, Tag
from backend import settings


class GolosCommand(BaseCommand):
    """
    Class to handle interaction with golos blockchain, like posting
    """

    def handle(self, *args, **options):
        posts = Post.objects.filter(is_published=False)

        # todo add url
        meta = {'app': 'URL'}
        # Send to Golos all not published posts
        for post in posts:
            if post.project is None:
                post = post.worker
            else:
                post = post.project

            steem = Steem(post.master_node)
            steem.wallet.setKeys(settings.ITSPHERE_POSTING_KEY)
            # Get post tags
            tags = post.tags
            # Mark post with ITSphere tag
            itsphere_tag = Tag.objects.get_or_create(name='itsphere')[0]
            if itsphere_tag not in tags:
                tags.append(itsphere_tag)
            try:
                if settings.POST_TO_BLOCKCHAIN:
                    steem.post(
                        title=post.title,
                        body=post.post.body,
                        author='ITSphere',
                        permlink=post.permlink,
                        meta=meta,
                        tags=tags
                    )
                post.is_published = True
            except Exception:
                post.is_published = False
            post.save()
