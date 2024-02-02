from django.contrib import admin

from dukan.models import Category, Product, PaymentMethod, Payment

all_models = [Category, Product, PaymentMethod]
admin.site.register(all_models)
