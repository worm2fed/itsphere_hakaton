from django.core.management import BaseCommand
from piston.steem import Steem

from apps.auth_api.models import Post, Tag
from backend import settings


class PostCommand(BaseCommand):
    """
    Command to send posts to Golos blockchain
    """
    def handle(self, *args, **options):
        posts = Post.objects.filter(is_published=False)
        # Send to Golos all not published posts
        for post in posts:
            if post.project is None:
                post = post.worker
            else:
                post = post.project

            steem = Steem(node=settings.NODE_URL, wif=settings.POSTING_KEY)
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
                        author=settings.POST_AUTHOR,
                        permlink=post.permlink,
                        parentPermlink='ITSphere',
                        tags=tags,
                        metadata=post.post.metadata
                    )
                post.is_published = True
            except Exception:
                post.is_published = False
            post.save()
