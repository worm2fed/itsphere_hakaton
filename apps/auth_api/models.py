<<<<<<< HEAD
=======
from django.core.exceptions import ValidationError
>>>>>>> ae90e36b344f1bc27c6f4e7e628ae2cc8dace611
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from transliterate import translit


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
<<<<<<< HEAD
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username, **extra_fields)
=======
        user = self.model(email=email, **extra_fields)
>>>>>>> ae90e36b344f1bc27c6f4e7e628ae2cc8dace611
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(**extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, null=True)
<<<<<<< HEAD
    email = models.EmailField('email address', unique=True, blank=True, null=True)
    bitcoin_address = models.CharField(max_length=150, null=True)

    contacts = models.CharField(max_length=250, null=True)
    languages = models.CharField(max_length=250, null=True)
    message = models.CharField(max_length=1024, null=True)
    locale = models.CharField(max_length=100, choices=LOCALE_CHOICES, default=LOCALE_CHOICES[0][0])
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, max_length=500)


    posting_key = models.CharField(max_length=150, blank=True, null=True)

    auto_update_position = models.BooleanField(default=True)
    now_not_in_position = models.BooleanField(default=False)
=======
    email = models.EmailField('email address', unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
>>>>>>> ae90e36b344f1bc27c6f4e7e628ae2cc8dace611

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('manager', default=False)

    is_employer = models.BooleanField('employer', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
<<<<<<< HEAD
        return self.username or self.email

    def get_full_name(self):
        return '{}: {}'.format(self.name, self.email)
=======
        return self.email

    def get_full_name(self):
        return '{}: {}'.format(self.username, self.email)
>>>>>>> ae90e36b344f1bc27c6f4e7e628ae2cc8dace611

    def get_short_name(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    """
    This model represents post about project
    """
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag, blank=True)
    is_for_team = models.BooleanField(default=False)
    github_link = models.URLField(blank=True)
    gitlab_link = models.URLField(blank=True)
    bitbucket_link = models.URLField(blank=True)
    golos_link = models.URLField(blank=False)

<<<<<<< HEAD

class BlockChain(models.Model):
    master_node = models.CharField(max_length=100)
    locale = models.CharField(max_length=5)
    blockchain = models.CharField(max_length=15)

    def __str__(self):
        return '%s' % self.locale

    def get_locale(self):
        if not BlockChain.objects.all().exists():
            BlockChain.objects.get_or_create(locale='ru', master_node='wss://ws.mapala.net', blockchain='golos')
            BlockChain.objects.get_or_create(locale='en', master_node='wss://node.steem.ws', blockchain='steem')
        if not self.locale:
            self.locale = BlockChain.objects.get(locale='ru')
            self.save()
        return self.locale.locale
=======
    @property
    def body(self):
        """
        Helper to get post body for Golos posting
        :return: string
        """
        # TODO: build post body
        return self.description

    @property
    def metadata(self):
        """
        Helper to get metadata for posting to Golos
        :return: dict
        """
        return {
            'golos_link': self.golos_link,
            'github_link': self.github_link,
            'gitlab_link': self.gitlab_link,
            'bitbucket_link': self.bitbucket_link
        }


class Worker(models.Model):
    """
    This model represents post about worker
    """
    name = models.CharField(max_length=200, blank=False)
    about = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag, blank=True)
    is_team = models.BooleanField(default=False)
    golos_link = models.URLField(blank=False)

    @property
    def title(self):
        """
        Helper to get worker name as title for posting to Golos
        """
        return self.name

    @property
    def body(self):
        """
        Helper to get post body for Golos posting
        :return: string
        """
        # TODO: build post body
        return self.body

    @property
    def metadata(self):
        """
        Helper to get metadata for posting to Golos
        :return: dict
        """
        return {
            'golos_link': self.golos_link
        }


class Post(models.Model):
    """
    This model needed to easy handle posts. We have to kinds of post: project and worker. This models simply
    stores foreign key to post wanted to post
    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    permlink = models.SlugField(unique=True, null=True, max_length=255)

    @property
    def post(self):
        """
        Helper to get post instance - project or worker profile
        """
        if self.project is None:
            return self.worker
        else:
            return self.project

    def save(self, *args, **kwargs):
        # Check iff only one link provided
        if self.project is None and self.worker is None:
            raise ValidationError("You have to link post to project or profile")
        if self.project is not None and self.worker is not None:
            raise ValidationError("You can specify only one of project or profile links")

        # Check is permlink was set
        if not self.permlink:
            slug = slugify(translit(self.post.title, 'ru', reversed=True))
            unique_slug = slug

            num = 1
            # Prepare slug
            while self.objects.filter(permlink=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, num)
                num += 1
            self.permlink = unique_slug
        super().save()

    @property
    def tags(self):
        """
        Helper to get post tags
        :return: list
        """
        return [t.name for t in self.post.tags.all()]
>>>>>>> ae90e36b344f1bc27c6f4e7e628ae2cc8dace611
