import jwt

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def check_credentials(self, username, email):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username and password."""
        self.check_credentials(username, email)
        user = self.model(username=username, email=self.normalize_email(email),)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser powers.

        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
    
    def create_writer(self, username, email, password):
        """Create and return a user with writer priviledges. """
        user = self.create_user(username, email, password)
        user.is_writer = True
        user.save()
        return user

    def create_client(self, username, email, password):
        """Create and return a user with client priviledges. """
        user = self.create_user(username, email, password)
        user.is_client = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_writer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
 
    @property
    def token(self):
        return self.generate_jwt_token()
 
    def get_short_name(self):
        return self.username

    def generate_jwt_token(self):
        """ Generates a token that expires in 24hrs """
        token = jwt.encode({
            "email": self.email,
            "username": self.username,
            "exp": datetime.utcnow()
            + timedelta(hours=24)
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def __str__(self):
        return self.email
