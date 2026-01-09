
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect

from .models import ItemModel
from .forms import UserRegisterForm,UserLoginForm



def all_items(request):
    items = ItemModel.objects.all()
    return render(request,'quickstart/items/item.html', {
        'items' : items
    })


def login_views(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('quickstart:items_list')
            else:
                form.add_error(None,'Неверный логин или пароль!')
    else:
        form = UserLoginForm()

    return render(request, 'quickstart/auth/login.html', {'form' : form})


def register_views(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('quickstart:login_user')
    else:
        form = UserRegisterForm()

    return render(request, 'quickstart/auth/register.html', {'form' : form})