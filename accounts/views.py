from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from find_route.accounts.forms import UserLogInForm, UserRegistrationForm


def login_view(request):
    """Функция входа пользователя в аккаунт"""
    form = UserLogInForm(request.POST or None)
    _next = request.GET.get('next')  # Ключ страницы, с которой пришел пользователь
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)  # Ввод в систему
        _next = _next or 'home'
        return redirect(_next)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)  # commit=False - Пользователь не до конца сохранен
            new_user.set_password(form.cleaned_data['password'])  # Шифрует пароль
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})
