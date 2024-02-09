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
    image_list = file_data.getlist('image_files[]', [])

    product = Product.objects.filter(id=prd_id).first()

    if product:
        for count, f in enumerate(image_list):
            if f and not hlp.upload_product_image(f, prd_id, count+1):
                context['message'] = 'error while saving image on disk'
                return render(request, 'dukan/product.html', context)


    return redirect("dukan:view_all_product")



@csrf_protect
@require_http_methods(["GET", "POST"])
def category_products(request, ctgry_id):
    ''' view products of a category into sitaram application '''

    if request.method == "GET":

        selected = Product.objects.filter(category=ctgry_id)
        selected_json = serializers.serialize('json', selected)

        return HttpResponse(selected_json, content_type='application/json')



@csrf_protect
@login_required
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
@login_required
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
        ordered_qty = order.order_quantity.split(',')
        for index, product in enumerate(order.order_products.all()):
            product.avl_qty = product.avl_qty - float(ordered_qty[index])
            product.save()

        order.order_status = False
        order.save()

    return redirect("dukan:view_orders")


@csrf_protect
@login_required
@require_http_methods(["GET"])
def delete_order(request, order_id):
    ''' view to confirm order into sitaram application '''
    context = {}

    order = Order.objects.filter(id=order_id).first()

    if order:
        order.delete()

    return redirect("dukan:view_orders")


@csrf_protect
@login_required
@require_http_methods(["GET"])
def cancel_order(request, order_id):
    ''' view to confirm order into sitaram application '''
    context = {}

    order = Order.objects.filter(id=order_id).first()

    if order:
        order.delete()

    return redirect("dukan:view_orders")    


@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def upload_products(request):
    ''' view to confirm order into sitaram application '''
    context = {}

    if request.method == "GET":
        return render(request, 'dukan/upload.html', context)

    file_data = request.FILES
    f = file_data.get('products_file', None)
    
    if f and hlp.handle_uploaded_file(f, rename='products.txt'):

        products_data_list = hlp.data_from_file('products.txt')
        header_flag = True

        for prod_data_line in products_data_list:
            splited_words = prod_data_line.split('||')
            remove_space = lambda x : x.strip(' \n')
            splited_words = list(map(remove_space, splited_words))

            if not header_flag and len(splited_words) == 7:
                category_code = splited_words[1]
                category_name = splited_words[2]
                product_name = splited_words[3]
                product_cost = splited_words[4]
                product_unit = splited_words[5]
                product_avl_qty = splited_words[6]
                

                category, created = Category.objects.get_or_create(added_by=request.user, code=category_code)

                if created:
                    category.name = category_name

                product, created = Product.objects.get_or_create(added_by=request.user, category=category, name=product_name)

                try:
                    product.cost = float(product_cost)
                    product.avl_qty = int(product_avl_qty)
                except Exception:
                    pass

                product.unit = product_unit
                product.save()


            if header_flag and 'PROD_ID' in splited_words and 'CATEGORY_CODE' in splited_words and 'PRODUCT_NAME' in splited_words:
                header = splited_words
                header_flag = False

        return redirect("dukan:view_all_product")
    else:
        context['message'] = 'error while uploading products'
        return render(request, 'dukan/upload.html', context)


@csrf_protect
@login_required
@require_http_methods(["GET", "POST"])
def download_products(request):
    ''' view to confirm order into sitaram application '''
    context = {}

    if request.method == "GET":
        return render(request, 'dukan/download.html', context)

    

    if request.method == "POST":
        products_file = "products.txt"

        header = "PROD_ID || CATEGORY_CODE   ||  CATEGORY_NAME  || PRODUCT_NAME  ||  PRODUCT_COST || PRODUCT_UNIT  || PRODUCT_QTY"

        all_products = Product.objects.all()

        all_products_list = [header]

        for counter, product in enumerate(all_products):
            category_code = str(product.category.code)
            category_name = str(product.category.name)
            product_name = str(product.name)
            product_cost = str(product.cost)
            product_unit = str(product.unit)
            product_avl_qty = str(product.avl_qty)

            all_products_list.append("||".join([str(counter), category_code, category_name, product_name, product_cost, product_unit, product_avl_qty]))

        if len(all_products_list) == 1:
            products_file = "template.txt"
            all_products_list.append("||".join([str(1), 'FRT', 'Fruits', 'Apple', '100', 'kg', '100']))
            all_products_list.append("||".join([str(2), 'FRT', 'Fruits', 'Mango', '100', 'kg', '100']))
            all_products_list.append("||".join([str(3), 'SBJ', 'Sabjiya', 'Matar', '50', 'kg', '50']))
            all_products_list.append("||".join([str(4), 'SBJ', 'Sabjiya', 'Tamatar', '50', 'kg', '40']))
            all_products_list.append("||".join([str(4), 'ALL', 'General', 'Pen', '10', 'pc', '60']))
            all_products_list.append("||".join([str(4), 'ALL', 'General', 'Pencil', '5', 'pc', '90']))


        all_products_content = "\n".join(all_products_list)

        response = HttpResponse(all_products_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(products_file)
        return response

    else:
        context['message'] = 'error while downloading products'
        return render(request, 'dukan/download.html', context)


@csrf_protect
@require_http_methods(["GET"])
def about_dukan(request):
    ''' view products of a category into sitaram application '''

    context = {}

    return render(request, 'dukan/aboutus.html', context)
