
import json

from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.http import JsonResponse

from .models import ItemModel,OrderModel
from .forms import UserRegisterForm,UserLoginForm



def all_items(request):
    items = ItemModel.objects.all()
    if request.user.is_authenticated:
        return render(request,'quickstart/items/item.html', {
            'items' : items
        })
    return render(request,'quickstart/auth/notlogin.html')


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


def add_item_to_cart(request):
    data = json.loads(request.body)
    
    order = OrderModel.objects.create(
        user = request.user,
        is_paid = False
    )

    item = ItemModel.objects.get(id = data['item_id'])
    order.items.add(item)

    return JsonResponse({
        'message' : 'ok'
    })


def cart_view(request):
    if request.user.is_authenticated:
        orders_user = OrderModel.objects.filter(user=request.user)
        items = ItemModel.objects.filter(orders__in=orders_user).distinct()

        return render(request,'quickstart/cart/cart.html', {
            'items' : items
        })
    return render(request,'quickstart/auth/notlogin.html')

def remove_item_from_cart(request, item_id):
    order = OrderModel.objects.filter(
        user=request.user,
        items__id=item_id,
        is_paid=False
    ).first()

    if not order:
        return JsonResponse({'success': False})

    order.items.remove(item_id)
    return JsonResponse({'success': True})