from django.urls import path
from django.views.generic.base import TemplateView
from .views import UserLoginView, SignUpView, UserLogoutView, ForgotPasswordView, ForgotLoginIdView, UpdateAccountDetailsView
#  UserAccountDetailsView,
app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # path('account-details/', UserAccountDetailsView.as_view(), name='account_details'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('forgot-login-id/', ForgotLoginIdView.as_view(), name='forgot_login_id'),
    path('update-account-details/', UpdateAccountDetailsView.as_view(), name='update_account_details'),
]