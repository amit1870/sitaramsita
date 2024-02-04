from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from dukan import views

app_name = 'dukan'

urlpatterns = [
    path("products/", views.view_all_product, name="view_all_product"),
    path("products/<int:prd_id>", views.update_product, name="update_product"),
    path("save/", views.save_product, name="save_product"),
    path("categorys/<int:ctgry_id>", views.category_products, name="category_products"),
    
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/<int:prd_id>", views.add_product_in_cart, name="add_product_in_cart"),

    path("orders/", views.view_orders, name="view_orders"),
    path("order/", views.process_cart, name="process_cart"),
    path("order/<int:order_id>/confirm", views.confirm_order, name="confirm_order"),
    path("order/<int:order_id>/pay", views.order_payment, name="order_payment"),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)