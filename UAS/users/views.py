from django.shortcuts import render
from .services import UserServiceImpl

def login_view(request):
    if request.method == 'POST':
        login_id = request.POST.get('login_id')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user_service = UserServiceImpl(request)
        response = user_service.user_login(login_id, password, role)
        return response

    return render(request, 'login.html')
