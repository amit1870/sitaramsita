from django.contrib import admin

from dukan.models import Category, Product, Cart, CartTemplate, Order, PaymentMethod, Payment

all_models = [Category, Product, Cart, CartTemplate, Order, PaymentMethod, Payment]
admin.site.register(all_models)
