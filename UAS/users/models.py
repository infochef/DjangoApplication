import logging
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Configure logging
logger = logging.getLogger(__name__)

class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    login_id = models.CharField(_("Login ID"), max_length=50, unique=True)
    password = models.CharField(_("Password"), max_length=128)  # Increased max_length for hashed passwords
    role = models.CharField(_("Role"), max_length=20)
    email = models.EmailField(_("Email ID"), max_length=254, validators=[EmailValidator()])
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user_data'  # Changed to snake_case for convention
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.login_id} ({self.role})"

    def clean(self):
        #"""Custom validation to ensure valid data before saving."""
        super().clean()
        
        # Validate the role field
        valid_roles = ['admin', 'user', 'manager']
        if self.role not in valid_roles:
            logger.error(f"Validation error: Invalid role '{self.role}'. Must be one of {valid_roles}.")
            raise ValidationError(f"Invalid role '{self.role}'. Must be one of {valid_roles}.")

    def save(self, *args, **kwargs):
        #"""Override save method to add logging."""
        try:
            self.clean()  # Call custom validation
            super().save(*args, **kwargs)
            logger.info(f"User saved successfully: {self.login_id}")
        except ValidationError as e:
            logger.error(f"Validation error while saving user {self.login_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while saving user {self.login_id}: {e}")
            raise


