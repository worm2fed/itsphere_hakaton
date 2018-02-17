from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

LOCALE_CHOICES = (
    ('ru', 'Русский'),
    ('en', 'English')
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')

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


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, null=True)
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

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('manager', default=False)

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
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


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
