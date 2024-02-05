from django.contrib import admin

from dukan.models import Category, Product, PaymentMethod, DukanDetail

all_models = [Category, Product, PaymentMethod, DukanDetail]
admin.site.register(all_models)
