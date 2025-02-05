from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib import messages
from .models import Supplier, WaterBottle, Account

# Create your views here.

# Account registration/authentication

def login(request):
    if(request.method=="POST"):
        user = request.POST.get('user')
        passw = request.POST.get('pass')
        try:
            acct = Account.objects.get(username=user)
            if acct.password == passw:
                a = acct.pk
                return redirect('view_supplier', pk=a)
            else:
                messages.error(request, "Invalid login. Please try again.")
                return redirect('login')
        except:
            messages.error(request, "Invalid login. Please try again.")
            return redirect('login')
    else:
        return render(request, 'Myinventoryapp/login.html')

def signup(request):
    if(request.method=="POST"):
        user = request.POST.get('user')
        passw = request.POST.get('pass')
        try:
            Account.objects.create(username=user, password=passw)
            messages.success(request, "Account successfully created!")
            return redirect('login')
        except:
            messages.error(request, "An account with this username already exists. Please try again.")
            return redirect('signup')
    else:
       return render(request, 'Myinventoryapp/signup.html')
    
# Account management
    
def manage_account(request, pk):
    a = get_object_or_404(Account, pk=pk)
    return render(request, 'Myinventoryapp/manage_account.html', {'a':a})

def delete_account (request, pk):
    Account.objects.filter(pk=pk).delete()
    return redirect('login')

def change_password (request, pk):
    a = get_object_or_404(Account, pk=pk)
    if(request.method=="POST"):
        current = request.POST.get('current_pass')
        new = request.POST.get('new_pass')
        retype = request.POST.get('retype_pass')
        if current == a.password:
            if new == retype:
                Account.objects.filter(pk=pk).update(password=new)
                return redirect('manage_account', pk=a.pk)
            else:
                messages.error(request, "Password is invalid, please tryy again.")
                return redirect('change_password', pk=a.pk)
        else:
            messages.error(request, "Password is invalid, please try again.")
            return redirect('change_password', pk=a.pk)
    else:
        return render(request, 'Myinventoryapp/change_password.html', {'a':a})

# Bottle/Supplier info

def view_supplier(request, pk):
    a = get_object_or_404(Account, pk=pk)
    supplier_objects = Supplier.objects.all()
    context = {'supplier':supplier_objects,
               'a':a}
    return render(request, 'Myinventoryapp/view_supplier.html', context)

def view_bottles(request, pk):
    a = get_object_or_404(Account, pk=pk)
    bottle_objects = WaterBottle.objects.all()
    context = {'bottle':bottle_objects,
               'a':a}
    return render(request, 'Myinventoryapp/view_bottles.html', context)

def add_bottle(request, pk):
    a = get_object_or_404(Account, pk=pk)
    supplier_objects = Supplier.objects.all()
    context = {'supplier':supplier_objects,
               'a':a}
    if(request.method=="POST"):
        try:
            sku = request.POST.get('sku')
            brand = request.POST.get('brand')
            cost = request.POST.get('cost')
            size = request.POST.get('size')
            mouth_size = request.POST.get('mouth_size')
            color = request.POST.get('color')
            supplierpk = request.POST.get('supplied_by')
            current_quantity = request.POST.get('current_quantity')

            supplier = Supplier.objects.get(pk=supplierpk)

            WaterBottle.objects.create(sku=sku, brand=brand, cost=cost, size=size, mouth_size=mouth_size, color=color, supplied_by=supplier, current_quantity=current_quantity)
            return redirect('view_bottles', pk=a.pk)
        except:
            return redirect('add_bottle', pk=a.pk)
    else:
        return render(request, 'Myinventoryapp/add_bottle.html', context)

def view_bottle_details(request, pk, pk_bottle):
    a = get_object_or_404(Account, pk=pk)
    b = get_object_or_404(WaterBottle, pk=pk_bottle)
    context = {'a': a,
               'b': b}
    return render(request, 'Myinventoryapp/view_bottle_details.html', context)

def delete_bottle(request, pk, pk_bottle):
    a = get_object_or_404(Account, pk=pk)
    WaterBottle.objects.filter(pk=pk_bottle).delete()
    return redirect('view_bottles', pk=a.pk)