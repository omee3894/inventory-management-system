from django.contrib import admin
from .models import Product

admin.site.register(Product)

from .models import Stock

admin.site.register(Stock)