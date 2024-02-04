from django.contrib import admin

from dukan.models import Category, Product, PaymentMethod, Order

all_models = [Category, Product, PaymentMethod, Order]
admin.site.register(all_models)
