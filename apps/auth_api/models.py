# coding:utf-8
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

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(u'Email должен быть установлен')

        # if 'fio' in extra_fields:
        #   fio = extra_fields['fio']
        # else:
        #   fio = None
        user = self.model(email=email, **extra_fields)
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
    email = models.EmailField('email address', unique=True, blank=False, null=False)
    fio = models.CharField(max_length=200, unique=False, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, max_length=500)

    auto_update_position = models.BooleanField(default=True)
    now_not_in_position = models.BooleanField(default=False)

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('manager', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

    def __str__(self):
        v=self.email
        if not v:
          v = 'no email'
        return v

    def get_full_name(self):
        return '{}: {}'.format(self.fio, self.email)

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url


# class BlockChain(models.Model):
#     master_node = models.CharField(max_length=100)
#     locale = models.CharField(max_length=5)
#     blockchain = models.CharField(max_length=15)

#     def __str__(self):
#         return '%s' % self.locale

#     def get_locale(self):
#         return None
