from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse


from django.shortcuts import render, redirect
from django.core import serializers

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


from dukan.models import Category, Product, Cart, CartTemplate, Order
from utils import helper as hlp



@csrf_protect
@require_http_methods(["GET", "POST"])
def view_all_product(request):
    ''' view products of a category into sitaram application '''

    context = {}

    categorys = Category.objects.all()
    products = Product.objects.all()

    context['products'] = products
    context['categorys'] = categorys

    return render(request, 'dukan/products.html', context)




@csrf_protect
@require_http_methods(["GET", "POST"])
def category_products(request, ctgry_id):
    ''' view products of a category into sitaram application '''

    if request.method == "GET":

        selected = Product.objects.filter(category=ctgry_id)
        selected_json = serializers.serialize('json', selected)

        return HttpResponse(selected_json, content_type='application/json')



@csrf_protect
@require_http_methods(["POST"])
def add_product_in_cart(request, prd_id):
    ''' view to add product in cart into sitaram application '''

    context = {}

    if request.method == "POST":

        product = Product.objects.filter(id=prd_id).first()

        if product:
            cart, created = Cart.objects.get_or_create(added_by=request.user)
            cart.products.add(product)
            cart.total_cost = cart.total_cost + product.cost
            cart.save()

        return redirect("dukan:view_all_product")



@csrf_protect
@require_http_methods(["GET", "POST"])
def view_cart(request):
    ''' view to add product in cart into sitaram application '''

    context = {}

    if request.method == "GET":
        cart, created = Cart.objects.get_or_create(added_by=request.user)
        context['cart'] = cart
        return render(request, 'dukan/cart.html', context)
