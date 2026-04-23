from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, Stock, Bill
def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')
from django.contrib.auth.decorators import login_required

@login_required

def dashboard(request):
    from .models import Bill
    
    total_sales = sum(b.total_price for b in Bill.objects.all())
    total_orders = Bill.objects.count()

    return render(request, 'dashboard.html', {
        'total_sales': total_sales,
        'total_orders': total_orders
    })

from .models import Product, Stock

def add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        quantity = request.POST['quantity']

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity
        )

        return redirect('/products')

    return render(request, 'add_product.html')

from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

from django.shortcuts import get_object_or_404

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('/products')

def edit_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.save()

        return redirect('/products')

    return render(request, 'edit_product.html', {'product': product})

def update_stock(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        quantity = int(request.POST['quantity'])
        action = request.POST['action']

        if action == "IN":
            product.quantity += quantity
        elif action == "OUT":
            product.quantity -= quantity

        product.save()

        Stock.objects.create(
            product=product,
            type=action,
            quantity=quantity
        )

        return redirect('/products')

    return render(request, 'stock.html', {'product': product})

from .models import Product, Bill

def billing(request):
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST['product']
        quantity = int(request.POST['quantity'])

        product = Product.objects.get(id=product_id)

        total = product.price * quantity

        # reduce stock
        product.quantity -= quantity
        product.save()

        # save bill
        Bill.objects.create(
            product=product,
            quantity=quantity,
            total_price=total
        )

        return render(request, 'bill.html', {
            'product': product,
            'quantity': quantity,
            'total': total
        })

    return render(request, 'billing.html', {'products': products})

from django.contrib.auth.models import User

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_user(username='admin', password='admin123')
    return HttpResponse("Admin created")