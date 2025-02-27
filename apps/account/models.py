from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("A valid email address is required.")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
        ("merchant", "Merchant"),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="profiles", null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="user")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return False
