from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
import logging

# Configure logging
logger = logging.getLogger(__name__)

class CustomUserManager(BaseUserManager):
    def create_user(self, login_id, password=None, role='user', **extra_fields):
        """
        Create and return a regular user with a login_id, password, and role.
        """
        if not login_id:
            raise ValueError('The Login ID field must be set')
        
        if role not in ['admin', 'user', 'manager']:
            raise ValueError('The role must be one of admin, user, or manager.')
        
        user = self.model(login_id=login_id, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id, password=None, **extra_fields):
        """
        Create and return a superuser with a login_id, password, and default role.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Ensure superusers have the admin role

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(login_id, password, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    login_id = models.CharField(_("Login ID"), max_length=50, unique=True)
    password = models.CharField(_("Password"), max_length=128)
    role = models.CharField(_("Role"), max_length=20, default='user')
    email = models.EmailField(_("Email ID"), max_length=254, default="Unknown", validators=[EmailValidator()])
    first_name = models.CharField(_("First Name"), max_length=50, default="Unknown")
    last_name = models.CharField(_("Last Name"), max_length=50, default="Unknown")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user_data'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.login_id} ({self.role})"

    def clean(self):
        super().clean()
        
        valid_roles = ['admin', 'user', 'manager']
        if self.role not in valid_roles:
            logger.error(f"Validation error: Invalid role '{self.role}'. Must be one of {valid_roles}.")
            raise ValidationError(f"Invalid role '{self.role}'. Must be one of {valid_roles}.")

    def save(self, *args, **kwargs):
        try:
            self.clean()
            super().save(*args, **kwargs)
            logger.info(f"User saved successfully: {self.login_id}")
        except ValidationError as e:
            logger.error(f"Validation error while saving user {self.login_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while saving user {self.login_id}: {e}")
            raise

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission.
        """
        # Add custom permission logic here
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has permissions to view the app `app_label`.
        """
        # Add custom logic to check app permissions here
        return True
