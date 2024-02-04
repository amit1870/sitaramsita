from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse


from django.shortcuts import render, redirect
from django.core import serializers

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


from dukan.models import Category, Product, Cart, CartTemplate, Order, PaymentMethod
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
@login_required
@require_http_methods(["GET"])
def update_product(request, prd_id):
    ''' view products of a category into sitaram application '''

    context = {}

    product = Product.objects.filter(id=prd_id).first()

    if request.method == "GET":
        if product:
            context['product'] = product
            return render(request, 'dukan/product.html', context)
        else:
            return render(request, 'dukan/dukan_404.html', context)
    

@csrf_protect
@login_required
@require_http_methods(["POST"])
def save_product(request):
    ''' view products of a category into sitaram application '''

    context = {}

    file_data = request.FILES
    form_data = request.POST.copy()

    prd_id = form_data.get('image_id', 0)
    f = file_data.get('image_file', None)
    
    if f and hlp.handle_uploaded_file(f, prd_id):
        return redirect("dukan:view_all_product")
    else:
        context['message'] = 'error while saving image on disk'
        return render(request, 'dukan/product.html', context)




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

        payment = form_data.get('payment', 'PSPD')

        if payment == 'PRPD':
            context = {}
            payment_via = PaymentMethod.objects.all()
            context['order'] = order
            context['payments'] = payment_via
            return render(request, 'dukan/payment.html', context)


    return redirect("dukan:view_orders")




@csrf_protect
@login_required
@require_http_methods(["POST"])
def order_payment(request, order_id):
    ''' view orders placed into sitaram application '''

    context = {}

    form_data = request.POST.copy()

    order_cost = form_data.get('order_cost', 0)
    paid_amount = form_data.get('paid_amount', 0)
    payment_string = form_data.get('payment_string', '')
    help_text = form_data.get('help_text', '')

    order_cost = float(order_cost)
    paid_amount = float(paid_amount)

    if order_cost > 0 and (order_cost - paid_amount) <= 10:

        order = Order.objects.get(id=order_id)

        if order and (order.order_cost - order_cost) <= 1:
            order.payment_string = payment_string
            order.payment = 'PRPD'
            order.save()
        else:
            return render(request, 'dukan/dukan_404.html', context)
    else:
        return render(request, 'dukan/dukan_404.html', context)

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


@csrf_protect
@login_required
@require_http_methods(["GET"])
def confirm_order(request, order_id):
    ''' view to confirm order into sitaram application '''
    context = {}

    order = Order.objects.filter(id=order_id).first()

    if order:
        order.order_status = False
        order.save()

    return redirect("dukan:view_orders")

