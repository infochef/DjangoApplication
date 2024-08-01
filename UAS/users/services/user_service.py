import logging
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth import authenticate, get_user_model, login as django_login
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from .user import UserService
from ..models import Users

class UserServiceImpl(UserService):

    """ ==================================
    User Creation Functionality
    ======================================
     """
    def create_user(self, user_id, login_id, password, role, email, first_name, last_name):

        # Perfor basic validation
        if not all([user_id, login_id, password, role, email, first_name, last_name]):
            logger.error("Validation error: Missing required fields.")
            raise ValidationError("All fields are required.")
        
        if len(password) < 8:
            logger.error("Validation error: Password must be at least 8 characters long.")
            raise ValidationError("Password must be at least 8 characters long.")
        
        try:
            validate_email(email)
        except ValidationError:
            logger.error("Validation error: Invalid email address.")
            raise ValidationError("Invalid email address.")
    
        # Role Validation
        valid_roles = ['admin', 'user', 'manager']
        if role not in valid_roles:
             logger.error(f"Validation error: Invalid role '{role}'. Must be one of {valid_roles}.")
             raise ValidationError(f"Invalid role '{role}'. Must be one of {valid_roles}.")

        # Send confirmation email
        subject = 'Welcome to Our Service'
        message = f'Hi {first_name},\n\nThank you for registering. Your login ID is {login_id}.'
        from_email = 'your_outlook_email@outlook.com'
        try:
            send_mail(subject, message, from_email, [email])
            logger.info(f"Confirmation email sent to {email}")
        except BadHeaderError:
            logger.error("Invalid header found.")
            raise ValidationError("Invalid header found.")
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise Exception(f"Error sending email: {e}")
    
        try:
        
         # Create a new user instance
          user = Users(
                user_id=user_id,
                login_id=login_id,
                password=make_password(password),  # Hash the password before saving
                role=role,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
        
          # Validate the model instance fields
          user.full_clean()

          # Save the user instance to the database
          user.save()
          logger.info(f"User created successfully: {user_id}")
          return user
        
        except ValidationError as e:
            logger.error(f"Model validation error: {e}")
            raise ValidationError(f"Validation error: {e}")

        except IntegrityError as e:
            logger.error(f"Database integrity error: {e}")
            raise IntegrityError(f"Database error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"An unexpected error occurred: {e}")


    """ =================================
    User Login Functionality
    ================================== 
    """

    def user_login(self, login_id, password, role):
        try:
            # Validate inputs
            if not login_id or not password:
                logger.error("Login error: Missing login ID or password.")
                raise ValidationError("Login ID and password are required.")

            if not isinstance(login_id, str) or not isinstance(password, str):
                logger.error("Login error: Invalid data type for login ID or password.")
                raise ValidationError("Invalid data type for login ID or password.")
            
            # Authenticate user
            UserModel = get_user_model()
            user = authenticate(username=login_id, password=password)
            
            if user is None:
                logger.error("Login error: Invalid login ID or password.")
                raise ValidationError("Invalid login ID or password.")
            
            # Check if user role matches
            if user.role != role:
                logger.error(f"Login error: Role mismatch. Expected {role}, found {user.role}.")
                raise ValidationError("Role does not match.")

            # Log in the user and create a session
            django_login(self.request, user)
            logger.info(f"User logged in successfully: {login_id}")

            # Optionally return user or response
            return HttpResponse("Login successful.")

        except ValidationError as e:
            logger.error(f"Validation error during login: {e}")
            return HttpResponse(f"Error: {e}", status=400)

        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            return HttpResponse("An unexpected error occurred.", status=500)   
    
    """ ==================================
    Logout Functionality
    ================================== """

    @login_required
    def user_logout(self, request):
        """
        Logs out the user and redirects to the home page.
        """
        try:
            # Log the user out
            logout(request)
            logger.info(f"User with session {request.session.session_key} logged out successfully.")

            # Redirect to a success page or homepage
            return redirect('home')  # Replace 'home' with your redirect URL name

        except Exception as e:
            # Log any errors that occur during logout
            logger.error(f"Error during logout: {e}")
            raise ValidationError("An error occurred while logging out. Please try again.")


    """ ==============================
    User Account Details Functionality
    ============================== """

    def user_account_details(self, user_id, login_id, role, email, first_name, last_name):
        """
        Fetch and update user account details based on the provided parameters.

        :param user_id: Unique identifier for the user.
        :param login_id: New login ID for the user.
        :param role: New role for the user.
        :param email: New email address for the user.
        :param first_name: New first name for the user.
        :param last_name: New last name for the user.
        :return: Updated user instance.
        """
        # Perform basic validation
        if not all([user_id, login_id, role, email, first_name, last_name]):
            logger.error("Validation error: Missing required fields.")
            raise ValidationError("All fields are required.")

        if len(login_id) < 5:
            logger.error("Validation error: Login ID must be at least 5 characters long.")
            raise ValidationError("Login ID must be at least 5 characters long.")

        if len(first_name) < 2 or len(last_name) < 2:
            logger.error("Validation error: First name and last name must each be at least 2 characters long.")
            raise ValidationError("First name and last name must each be at least 2 characters long.")

        try:
            validate_email(email)
        except ValidationError:
            logger.error("Validation error: Invalid email address.")
            raise ValidationError("Invalid email address.")

        # Role Validation
        valid_roles = ['admin', 'user', 'manager']
        if role not in valid_roles:
            logger.error(f"Validation error: Invalid role '{role}'. Must be one of {valid_roles}.")
            raise ValidationError(f"Invalid role '{role}'. Must be one of {valid_roles}.")

        try:
            # Fetch the user based on user_id
            UserModel = get_user_model()
            user = UserModel.objects.filter(id=user_id).first()

            if user:
                # Update user details
                user.login_id = login_id
                user.role = role
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()  # Save the updated user details
                logger.info(f"User account details updated successfully for user_id: {user_id}")
                return user
            else:
                logger.error(f"User not found with user_id: {user_id}")
                raise ValidationError(f"User not found with user_id: {user_id}")

        except IntegrityError as e:
            logger.error(f"Database integrity error: {e}")
            raise IntegrityError(f"Database error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"An unexpected error occurred: {e}")
    

    
    """ ==============================
    Password Reset Functionality
    ============================== """

    def forgot_password(self, login_id, password, role):
        """
        Handle the password reset process for the given login_id.

        :param login_id: User's login ID.
        :param password: New password for the user.
        :param role: User's role (used for additional validation, if needed).
        :return: Message indicating the result of the operation.
        """
        # Basic validation
        if not login_id or not password or not role:
            logger.error("Validation error: Missing required fields.")
            raise ValidationError("Login ID, password, and role are required.")

        if len(password) < 8:
            logger.error("Validation error: Password must be at least 8 characters long.")
            raise ValidationError("Password must be at least 8 characters long.")

        # Role Validation (if needed)
        valid_roles = ['admin', 'user', 'manager']
        if role not in valid_roles:
            logger.error(f"Validation error: Invalid role '{role}'. Must be one of {valid_roles}.")
            raise ValidationError(f"Invalid role '{role}'. Must be one of {valid_roles}.")

        try:
            # Fetch the user by login_id
            UserModel = get_user_model()
            user = UserModel.objects.filter(login_id=login_id).first()

            if user:
                # Update the user's password
                user.set_password(password)  # Django method to handle password hashing
                user.save()  # Save the updated user details
                logger.info(f"Password reset successfully for login_id: {login_id}")

                # Optionally send an email notification (if applicable)
                subject = 'Password Reset Confirmation'
                message = f'Hi {user.first_name},\n\nYour password has been reset successfully.'
                from_email = 'your_outlook_email@outlook.com'
                try:
                    send_mail(subject, message, from_email, [user.email])
                    logger.info(f"Password reset confirmation email sent to {user.email}")
                except BadHeaderError:
                    logger.error("Invalid header found in the email.")
                    raise ValidationError("Invalid header found in the email.")
                except Exception as e:
                    logger.error(f"Error sending email: {e}")
                    raise Exception(f"Error sending email: {e}")

                return "Password reset successfully."

            else:
                logger.error(f"User not found with login_id: {login_id}")
                raise ValidationError(f"User not found with login_id: {login_id}")

        except IntegrityError as e:
            logger.error(f"Database integrity error: {e}")
            raise IntegrityError(f"Database error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"An unexpected error occurred: {e}")
        
    
        """ ==============================
    Login Id  Reset Functionality
    ============================== """

    def forgot_loginid(self, current_login_id, new_login_id, password, role):
        """
        Handle the update of the user's login ID.

        :param current_login_id: User's current login ID.
        :param new_login_id: New login ID to set for the user.
        :param password: Password to authenticate the user.
        :param role: User's role (used for additional validation, if needed).
        :return: Message indicating the result of the operation.
        """
        # Basic validation
        if not current_login_id or not new_login_id or not password or not role:
            logger.error("Validation error: Missing required fields.")
            raise ValidationError("Current login ID, new login ID, password, and role are required.")

        if len(new_login_id) < 5:
            logger.error("Validation error: New login ID must be at least 5 characters long.")
            raise ValidationError("New login ID must be at least 5 characters long.")

        # Role Validation (if needed)
        valid_roles = ['admin', 'user', 'manager']
        if role not in valid_roles:
            logger.error(f"Validation error: Invalid role '{role}'. Must be one of {valid_roles}.")
            raise ValidationError(f"Invalid role '{role}'. Must be one of {valid_roles}.")

        try:
            # Fetch the user by current_login_id
            UserModel = get_user_model()
            user = UserModel.objects.filter(login_id=current_login_id).first()

            if user:
                # Validate password
                if not user.check_password(password):
                    logger.error("Authentication error: Incorrect password.")
                    raise ValidationError("Incorrect password.")

                # Update the user's login ID
                user.login_id = new_login_id
                user.save()  # Save the updated user details
                logger.info(f"Login ID updated successfully from {current_login_id} to {new_login_id}.")

                # Optionally send a confirmation email (if applicable)
                # ...

                return "Login ID updated successfully."

            else:
                logger.error(f"User not found with current_login_id: {current_login_id}")
                raise ValidationError(f"User not found with current_login_id: {current_login_id}")

        except IntegrityError as e:
            logger.error(f"Database integrity error: {e}")
            raise IntegrityError(f"Database error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"An unexpected error occurred: {e}")
        

        """  =============================================
        Update Account Deatils Functionality
     ======================================================
    """
    

    def update_account_details(self, user_id, password, new_password=None, role=None, email=None, first_name=None, last_name=None):
        """
        Update user account details based on the provided parameters.

        :param user_id: Unique identifier for the user.
        :param password: Current password for authentication.
        :param new_password: New password for the user (optional).
        :param role: New role for the user (optional).
        :param email: New email address for the user (optional).
        :param first_name: New first name for the user (optional).
        :param last_name: New last name for the user (optional).
        :return: Message indicating the result of the operation.
        """
        # Basic validation
        if not user_id or not password:
            logger.error("Validation error: User ID and password are required.")
            raise ValidationError("User ID and password are required.")

        if new_password and len(new_password) < 8:
            logger.error("Validation error: New password must be at least 8 characters long.")
            raise ValidationError("New password must be at least 8 characters long.")

        if email:
            try:
                validate_email(email)
            except ValidationError:
                logger.error("Validation error: Invalid email address.")
                raise ValidationError("Invalid email address.")

        if role and role not in ['admin', 'user', 'manager']:
            logger.error(f"Validation error: Invalid role '{role}'. Must be one of ['admin', 'user', 'manager'].")
            raise ValidationError(f"Invalid role '{role}'. Must be one of ['admin', 'user', 'manager'].")

        try:
            # Fetch the user by user_id
            UserModel = get_user_model()
            user = UserModel.objects.filter(id=user_id).first()

            if user:
                # Authenticate the user
                if not user.check_password(password):
                    logger.error("Authentication error: Incorrect password.")
                    raise ValidationError("Incorrect password.")

                # Update the user's details
                if new_password:
                    user.set_password(new_password)  # Hash the new password
                if role:
                    user.role = role
                if email:
                    user.email = email
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name

                user.save()  # Save the updated user details
                logger.info(f"User account details updated successfully for user_id: {user_id}")

                return "Account details updated successfully."

            else:
                logger.error(f"User not found with user_id: {user_id}")
                raise ValidationError(f"User not found with user_id: {user_id}")

        except IntegrityError as e:
            logger.error(f"Database integrity error: {e}")
            raise IntegrityError(f"Database error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"An unexpected error occurred: {e}")
