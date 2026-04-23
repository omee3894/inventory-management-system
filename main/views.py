import json
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, Stock, Bill
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from .models import Sale
from django.utils.timezone import now
from datetime import timedelta
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
    today = now().date()

    # ---------- DAILY (last 7 days) ----------
    daily_labels = []
    daily_data = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        total = Sale.objects.filter(date=day).aggregate(
            Sum('total_price')
        )['total_price__sum'] or 0

        daily_labels.append(day.strftime("%d %b"))
        daily_data.append(float(total))

    # ---------- WEEKLY (last 4 weeks) ----------
    weekly_labels = []
    weekly_data = []

    for i in range(3, -1, -1):
        start = today - timedelta(days=(i + 1) * 7)
        end = today - timedelta(days=i * 7)

        total = Sale.objects.filter(date__range=[start, end]).aggregate(
            Sum('total_price')
        )['total_price__sum'] or 0

        weekly_labels.append(f"Week {4 - i}")
        weekly_data.append(float(total))

    # ---------- MONTHLY (last 6 months) ----------
    monthly_labels = []
    monthly_data = []

    for i in range(5, -1, -1):
        month = (today.month - i - 1) % 12 + 1
        year = today.year - ((today.month - i - 1) // 12)

        total = Sale.objects.filter(
            date__month=month,
            date__year=year
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0

        monthly_labels.append(f"{month}/{year}")
        monthly_data.append(float(total))

    # ---------- TOTAL ----------
    total_sales = sum(daily_data)
    total_orders = Sale.objects.count()

    return render(request, 'dashboard.html', {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),

        'weekly_labels': json.dumps(weekly_labels),
        'weekly_data': json.dumps(weekly_data),

        'monthly_labels': json.dumps(monthly_labels),
        'monthly_data': json.dumps(monthly_data),
    })

from .models import Product, Stock

def add_product(request):

    if not request.user.is_staff:
        return HttpResponse("Only admin allowed ❌")

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

    if not request.user.is_staff:
        return HttpResponse("Not allowed ❌")

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
from .models import Sale
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
        bill = Bill.objects.create(
            product=product,
            quantity=quantity,
            total_price=total
        )

        # save sale
        Sale.objects.create(
            product=product.name,
            quantity=quantity,
            total_price=total
        )

        # 👉 REDIRECT TO INVOICE PAGE
        return redirect('invoice', bill_id=bill.id)

    return render(request, 'billing.html', {'products': products})

from django.contrib.auth.models import User

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_user(username='admin', password='admin123')
    return HttpResponse("Admin created")

daily_sales = (
    Sale.objects
    .annotate(day=TruncDay('date'))
    .values('day')
    .annotate(total=Sum('total_price'))
    .order_by('day')
)

monthly_sales = (
    Sale.objects
    .annotate(month=TruncMonth('date'))
    .values('month')
    .annotate(total=Sum('total_price'))
    .order_by('month')
)
yearly_sales = (
    Sale.objects
    .annotate(year=TruncYear('date'))
    .values('year')
    .annotate(total=Sum('total_price'))
    .order_by('year')
)
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')
        return HttpResponse("Admin created")
    return HttpResponse("Already exists")
def invoice(request, bill_id):
    bill = Bill.objects.get(id=bill_id)
    return render(request, 'invoice.html', {'bill': bill})
