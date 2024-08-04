from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout as auth_logout
import logging
import json
from .services.user_service import UserServiceImpl

logger = logging.getLogger(__name__)
user_service = UserServiceImpl()

def handle_exception(e, message="An unexpected error occurred"):
    logger.error(f"{message}: {e}")
    return JsonResponse({'error': message}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    @method_decorator(csrf_protect)
    def post(self, request):
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decoding error: {e}")
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            data = request.POST

        try:
            user = user_service.sign_up(
                user_id=data.get('user_id'),
                login_id=data.get('login_id'),
                password=data.get('password'),
                role=data.get('role'),
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            logger.info(f"User signed up successfully: {user.user_id}")
            if request.content_type == 'application/json':
                return JsonResponse({'message': 'User created successfully', 'user_id': user.user_id}, status=201)
            else:
                return redirect('login')  # Redirect to the login page for browser-based requests
        except ValidationError as e:
            logger.warning(f"Validation error during sign-up: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return handle_exception(e)

    def get(self, request):
        csrf_token = get_token(request)  # Get CSRF token
        return render(request, 'signup.html', {'csrf_token': csrf_token})

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    @method_decorator(csrf_protect)
    def post(self, request):
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decoding error: {e}")
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
        else:
            data = request.POST

        try:
            response = user_service.user_login(
                request=request,
                login_id=data.get('login_id'),
                password=data.get('password'),
                role=data.get('role')
            )
            logger.info(f"User logged in successfully: {data.get('login_id')}")
            if request.content_type == 'application/json':
                return JsonResponse({'message': 'User logged in successfully'}, status=200)
            else:
                return redirect('home')  # Redirect to the home page for browser-based requests
        except ValidationError as e:
            logger.warning(f"Validation error during login: {e}")
            if request.content_type == 'application/json':
                return JsonResponse({'error': str(e)}, status=400)
            else:
                return render(request, 'login.html', {'error': str(e)})
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            if request.content_type == 'application/json':
                return JsonResponse({'error': 'Unexpected error during login'}, status=500)
            else:
                return render(request, 'login.html', {'error': 'Unexpected error during login'})

    def get(self, request):
        csrf_token = get_token(request)
        return render(request, 'login.html', {'csrf_token': csrf_token})

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(login_required, name='dispatch')
class UserLogoutView(View):
    def post(self, request):
        try:
            auth_logout(request)  # Call Django's logout function
            logger.info("User logged out successfully")
            if request.content_type == 'application/json':
                return JsonResponse({'message': 'User logged out successfully'}, status=200)
            else:
                return redirect('login')  # Redirect to login page for browser-based requests
        except ValidationError as e:
            logger.warning(f"Validation error during logout: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error during logout: {e}")
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)

    def get(self, request):
        csrf_token = get_token(request)
        return render(request, 'logout.html', {'csrf_token': csrf_token})

# @method_decorator(csrf_exempt, name='dispatch')
# class UserAccountDetailsView(LoginRequiredMixin, View):
#     @method_decorator(csrf_protect)
#     def get(self, request):
#         user_id = request.GET.get('user_id')  # Assuming user_id is passed as a query parameter
#         try:
#             user = user_service.get_user_details(user_id)
#             logger.info(f"Fetched user details for: {user_id}")
#             if request.content_type == 'application/json':
#                 return JsonResponse(user, status=200)
#             else:
#                 csrf_token = get_token(request)
#                 return render(request, 'account_details.html', {**user, 'csrf_token': csrf_token})
#         except ValidationError as e:
#             logger.warning(f"Validation error fetching account details: {e}")
#             return JsonResponse({'error': str(e)}, status=400)
#         except Exception as e:
#             return handle_exception(e)

#     @method_decorator(csrf_protect)
#     def post(self, request):
#         data = request.POST
#         try:
#             user = user_service.update_user_details(
#                 user_id=data.get('user_id'),
#                 login_id=data.get('login_id'),
#                 role=data.get('role'),
#                 email=data.get('email'),
#                 first_name=data.get('first_name'),
#                 last_name=data.get('last_name')
#             )
#             logger.info(f"Updated account details for user: {data.get('user_id')}")
#             if request.content_type == 'application/json':
#                 return JsonResponse({'message': 'User details updated successfully', 'user_id': user.user_id}, status=200)
#             else:
#                 return redirect('account_details')  # Redirect to account details page
#         except ValidationError as e:
#             logger.warning(f"Validation error during account details update: {e}")
#             return JsonResponse({'error': str(e)}, status=400)
#         except Exception as e:
#             return handle_exception(e)

@method_decorator(csrf_exempt, name='dispatch')
class ForgotPasswordView(View):
    @method_decorator(csrf_protect)
    def get(self, request):
        csrf_token = get_token(request)
        return render(request, 'forgot_password.html', {'csrf_token': csrf_token})

    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.POST
        try:
            message = user_service.forgot_password(
                login_id=data.get('login_id'),
                password=data.get('password'),
                role=data.get('role')
            )
            logger.info(f"Password reset successfully for login ID: {data.get('login_id')}")
            if request.content_type == 'application/json':
                return JsonResponse({'message': message}, status=200)
            else:
                return redirect('login')  # Redirect to login page after successful password change
        except ValidationError as e:
            logger.warning(f"Validation error during password reset: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return handle_exception(e)

@method_decorator(csrf_exempt, name='dispatch')
class ForgotLoginIdView(View):
    @method_decorator(csrf_protect)
    def get(self, request):
        csrf_token = get_token(request)
        return render(request, 'forgot_login_id.html', {'csrf_token': csrf_token})

    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.POST
        try:
            message = user_service.forgot_loginid(
                current_login_id=data.get('current_login_id'),
                new_login_id=data.get('new_login_id'),
                password=data.get('password'),
                role=data.get('role')
            )
            logger.info(f"Login ID changed successfully from {data.get('current_login_id')} to {data.get('new_login_id')}")
            if request.content_type == 'application/json':
                return JsonResponse({'message': message}, status=200)
            else:
                return redirect('login')  # Redirect to login page after successful login ID change
        except ValidationError as e:
            logger.warning(f"Validation error during login ID change: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return handle_exception(e)
        
       
@method_decorator(csrf_exempt, name='dispatch')
class UpdateAccountDetailsView(LoginRequiredMixin, View):
    @method_decorator(csrf_protect)
    def get(self, request):
        try:
            user = user_service.get_user_details(request.user.user_id)
            if not user:
                logger.warning(f"User not found for user_id: {request.user.user_id}")
                return JsonResponse({'error': 'User not found.'}, status=404)

            context = {
                'user_id': user.get('user_id'),
                'login_id': user.get('login_id'),
                'role': user.get('role'),
                'email': user.get('email'),
                'first_name': user.get('first_name'),
                'last_name': user.get('last_name'),
                'csrf_token': get_token(request)
            }
            logger.info(f"Fetched user details for update: {request.user.user_id}")
            return render(request, 'update_account_details.html', context)
        except ValidationError as e:
            logger.warning(f"Validation error during fetching user details for update: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        except ObjectDoesNotExist as e:
            logger.warning(f"User not found: {e}")
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            logger.error(f"Unexpected error during fetching user details: {e}")
            return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

    @method_decorator(csrf_protect)
    def post(self, request):
        data = request.POST
        try:
            message = user_service.update_account_details(
                user_id=request.user.user_id,
                password=data.get('password'),
                new_password=data.get('new_password'),
                role=data.get('role'),
                email=data.get('email'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )
            logger.info(f"Updated account details successfully for user ID: {request.user.user_id}")
            if request.content_type == 'application/json':
                return JsonResponse({'message': message}, status=200)
            else:
                return redirect('home')
        except ValidationError as e:
            logger.warning(f"Validation error during account details update: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error during account details update: {e}")
            return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)
