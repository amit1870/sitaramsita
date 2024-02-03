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


@csrf_protect
@login_required
@require_http_methods(["POST"])
def process_cart(request):
    ''' view to process cart loaded into sitaram application '''

    context = {}

    cart = Cart.objects.filter(added_by=request.user).first()

    if cart:
        form_data = request.POST.copy()
        cleaned_form_data = hlp.process_form_data(form_data)

        if cleaned_form_data:
            order_date = hlp.today_date()
            order = Order.objects.create(order_by=request.user, order_date=order_date)

            total_cost = 0
            order_quantity = []
            order_prices = []


            for prd_id, qty in cleaned_form_data.items():
                product = Product.objects.filter(id=prd_id).first()

                order.order_products.add(product)

                avl_qty = product.avl_qty
                if qty > avl_qty:
                    qty = avl_qty

                order_cost = qty * float(product.cost)

                total_cost = total_cost + order_cost

                product.avl_qty = avl_qty - qty
                product.save()

                order_quantity.append(str(qty))
                order_prices.append(str(product.cost))

                cart.products.remove(product)

            order_quantity = ",".join(order_quantity)
            order_prices = ",".join(order_prices)

            order.order_quantity = order_quantity
            order.order_prices = order_prices

            order.order_cost = total_cost
            order.save()


    return redirect("dukan:view_orders")


@csrf_protect
@login_required
@require_http_methods(["GET" , "POST"])
def view_orders(request):
    ''' view orders placed into sitaram application '''

    context = {}

    if request.user.is_superuser:
        all_orders = Order.objects.all()
    else:
        all_orders = Order.objects.filter(order_by=request.user)

    pending = [order for order in all_orders if order.order_status]
    context['pending'] = pending

    return render(request, 'dukan/orders.html', context)