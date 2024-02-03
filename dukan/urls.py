from django.urls import path

from dukan import views

app_name = 'dukan'

urlpatterns = [
    path("products/", views.view_all_product, name="view_all_product"),
    path("categorys/<int:ctgry_id>", views.category_products, name="category_products"),
    path("cart/<int:prd_id>", views.add_product_in_cart, name="add_product_in_cart"),
    path("orders/", views.view_orders, name="view_orders"),
    # path("order/<int:order_id>/confirm", views.confirm_order, name="confirm_order"),
    # path("categories/", views.dukan_categories, name="dukan_categories"),
    # path("categories/<int:ctgry_id>", views.category_products, name="category_products"),
    path("cart/", views.view_cart, name="view_cart"),
    # path("cart/<int:prd_id>", views.add_product_in_cart, name="add_product_in_cart"),
    path("order/", views.process_cart, name="process_cart"),
    # path("reports/", views.dukan_reports, name="dukan_reports"),
    # path("payments/", views.dukan_payments, name="dukan_payments"),
]