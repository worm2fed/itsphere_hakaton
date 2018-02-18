from django.core.management import BaseCommand

from apps.auth_api.models import Page


class Command(BaseCommand):
    """
    Command to send posts to Golos blockchain
    """
    def handle(self, *args, **options):
        pages = Page.objects.filter(is_published=False)
        # Send to Golos all not published posts
        for page in pages:
            page.post_to_golos()
