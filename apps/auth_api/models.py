from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
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

    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('manager', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '{}: {}'.format(self.fio, self.email)

    def get_short_name(self):
        return self.email

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url


class Project(models.Model):
    """
    This model represents post about project
    """


class Worker(models.Model):
    """
    This model represents post about worker
    """


class Post(models.Model):
    """
    This model needed to easy handle posts. We have to kinds of post: project and worker. This models simply
    stores foreign key to post wanted to post
    """
    project = models.ForeignKey('Project', on_delete=models.CASCADE, blank=True, null=True)
    worker = models.ForeignKey('Worker', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.project is None and self.worker is None:
            raise ValidationError("You have to link post to project or profile")
        if self.project is not None and self.worker is not None:
            raise ValidationError("You can specify only one of project or profile links")
        super(Post, self).save(*args, **kwargs)
