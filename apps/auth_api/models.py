from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from piston import Steem
from transliterate import translit

from backend import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    usage_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(**extra_fields)

    def get_queryset(self):
        return super(UserManager, self).get_queryset()


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, null=True)
    email = models.EmailField('email address', unique=True, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    name = models.CharField(max_length=200, blank=True)

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('manager', default=False)

    is_employer = models.BooleanField('employer', default=False)
    is_team = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, blank=True)
    golos_link = models.URLField(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username or self.email

    def get_full_name(self):
        return '{}: {}'.format(self.name, self.email)

    def get_short_name(self):
        return self.name


class Page(models.Model):
    author = models.ForeignKey(User)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_published = models.BooleanField(default=False)

    permlink = models.SlugField(unique=True, null=True, max_length=255)
    parent_permlink = models.CharField(max_length=1000, blank=True, null=True)

    title = models.CharField(max_length=1000)
    body = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.permlink:
            num = 1
            slug = slugify(translit(self.title, 'ru', reversed=True))
            unique_slug = slug

            while Page.objects.filter(permlink=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
            self.permlink = unique_slug
        self.post_to_golos()
        super().save()

    def get_tags(self):
        return [t.name for t in self.tags.all()]

    def get_tags_for_golos(self):
        golos_tags = [self.category.name]
        if self.author.is_employer:
            golos_tags.append('project')
        else:
            golos_tags.append('user')
        return golos_tags + self.get_tags()

    @property
    def metadata(self):
        """
        Helper to get metadata for posting to Golos
        :return: dict
        """
        return {
            'golos_link': self.author.golos_link,
        }

    def post_to_golos(self, is_repeat_request=False):
        """
        Method to post pages to Golos
        """
        # steem = Steem(node=settings.NODE_URL, wif=settings.POSTING_KEY)
        steem = Steem(node='wss://ws.golos.io', wif='5JgEDJqUKLSK6sD2rCqaPxZ2YAyaxTXmcqmp14WtWJ2BCpFzh4o')
        try:
            if settings.POST_TO_BLOCKCHAIN:
                steem.post(
                    title=self.title,
                    body=self.body,
                    author=settings.POST_AUTHOR,
                    # permlink=page.permlink,
                    tags=self.get_tags_for_golos(),
                    category=settings.POST_AUTHOR,
                    meta=self.metadata
                )
            self.is_published = True
        except Exception:
            self.is_published = False
        if is_repeat_request:
            self.save()
