from django.contrib import admin

from dukan.models import Category, Product, PaymentMethod, Order, Cart

all_models = [Category, Product, PaymentMethod, Order, Cart]
admin.site.register(all_models)
