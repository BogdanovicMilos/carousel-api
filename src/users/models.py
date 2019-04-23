import json
from django.db import models
from django.core.serializers import serialize
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


def upload_image(instance, filename):
    return 'avatar/{user}/{filename}'.format(user=instance.user, filename=filename)


class UserQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values('id', 'email', 'display_name', 'avatar'))
        return json.dumps(list_values)


class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def create_user(self, email, display_name, password=None):
        if not email:
            raise ValueError('User must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, display_name=display_name)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to=upload_image, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.display_name

    def serialize(self):
        try:
            avatar = self.avatar.url
        except:
            avatar = ''
        data = {
            'id': self.id,
            'email': self.email,
            'display_name': self.display_name,
            'avatar': avatar
        }
        data = json.dumps(data)
        return data
