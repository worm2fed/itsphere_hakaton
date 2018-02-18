from django.core.management import BaseCommand
from piston.steem import Steem

from apps.auth_api.models import Page, Tag
from backend import settings


class PostCommand(BaseCommand):
    """
    Command to send posts to Golos blockchain
    """
    def handle(self, *args, **options):
        pages = Page.objects.filter(is_published=False)
        # Send to Golos all not published posts
        for page in pages:
            steem = Steem(node=settings.NODE_URL, wif=settings.POSTING_KEY)
            # Get page tags
            tags = page.get_tags()
            # Mark page with ITSphere tag
            itsphere_tag = Tag.objects.get_or_create(name=settings.MAIN_TAG)[0]
            if itsphere_tag not in tags:
                tags.append(itsphere_tag)
            # Mark with tag for project or user
            if page.author.is_employer:
                type_tag = Tag.objects.get_or_create(name='project')[0]
            else:
                type_tag = Tag.objects.get_or_create(name='user')[0]
            if type_tag not in tags:
                tags.append(type_tag)
            try:
                if settings.POST_TO_BLOCKCHAIN:
                    steem.post(
                        title=page.title,
                        body=page.body,
                        author=settings.POST_AUTHOR,
                        permlink=page.permlink,
                        tags=tags,
                        meta=page.metadata
                    )
                page.is_published = True
            except Exception:
                page.is_published = False
            page.save()
