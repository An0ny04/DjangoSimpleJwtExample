from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusers must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusers must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class UserData(AbstractUser):
    username = None
    name = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
