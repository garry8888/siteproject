from django.shortcuts import render
from django.contrib.auth.models import User


def auth(request):
    if not request.user.is_authenticated:
        return render(request, 'users/login.html')
