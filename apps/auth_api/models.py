from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from transliterate import translit


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

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

    name = models.CharField(max_length=200, blank=False)

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('manager', default=False)

    is_employer = models.BooleanField('employer', default=False)
    is_team = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, blank=True)
    golos_link = models.URLField(blank=False)

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


class Post(models.Model):
    """
    This model needed to easy handle posts. We have to kinds of post: project and worker. This models simply
    stores foreign key to post wanted to post
    """
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    permlink = models.SlugField(unique=True, null=True, max_length=255)
    title = models.CharField(max_length=200, blank=False)
    body = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        # Check is permlink was set
        if not self.permlink:
            slug = slugify(translit(self.title, 'ru', reversed=True))
            unique_slug = slug

            num = 1
            # Prepare slug
            while self.objects.filter(permlink=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
            self.permlink = unique_slug
        super().save()

    def get_tags(self):
        """
        Helper to get post tags
        :return: list
        """
        return [t.name for t in self.tags.all()]

    @property
    def metadata(self):
        """
        Helper to get metadata for posting to Golos
        :return: dict
        """
        return {
            'golos_link': self.author.golos_link,
        }
