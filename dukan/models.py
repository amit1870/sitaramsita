from django.db import models
from django.contrib.auth import get_user_model

PAYMENT = [('PSPD', 'postpaid'),('PRPD', 'prepaid')]

def get_default_category():
    return Category.objects.get(code='ALL')

class Category(models.Model):
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='all', unique=True)
    code = models.CharField(max_length=5, default='ALL', unique=True)
    help_text = models.CharField(max_length=200, default='help text for category', unique=False)


    def __str__(self):
        return self.code



class Product(models.Model):
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET(get_default_category))
    help_text = models.CharField(max_length=200, default='help text for product', unique=False)
    name = models.CharField(max_length=50, unique=True)
    cost = models.DecimalField(max_digits=7,decimal_places=1, default=0)
    unit = models.CharField(max_length=3)
    avl_qty = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name



class PaymentMethod(models.Model):
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payee_name = models.CharField(max_length=255, blank=False)
    payee_mobile = models.CharField(max_length=10, blank=False)
    payee_medium = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.payee_name



class Payment(models.Model):
    payer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    payment_amount = models.PositiveIntegerField(blank=False)
    payment_mobile = models.CharField(max_length=10, blank=False)
    payment_date = models.DateField(auto_now_add=True)
    payment_string = models.CharField(max_length=255, blank=False, unique=True)
    help_text = models.CharField(max_length=200, default='help text for payment', unique=False)


    def __str__(self):
        return self.payment_string



class Order(models.Model):
    order_by = models.ForeignKey(get_user_model(), blank=True, null=True, on_delete=models.SET_NULL)
    order_date = models.DateField(auto_now_add=True)
    order_cost = models.PositiveIntegerField(default=0)
    order_status = models.BooleanField(default=True)
    order_products = models.ManyToManyField(Product)
    order_quantity = models.CharField(max_length=255, blank=False, null=False)
    order_prices = models.CharField(max_length=255, blank=False, null=False)
    payment = models.CharField(max_length=4, choices=PAYMENT, default='PSPD')
    payment_string = models.CharField(max_length=255, blank=True)
    

    def __str__(self):
        return self.order_by.name + self.order_by.mobile


class Cart(models.Model):
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=False, default='cart')
    help_text = models.CharField(max_length=200, default='help text for cart', unique=False)
    products = models.ManyToManyField(Product)
    total_cost = models.DecimalField(max_digits=10,decimal_places=1, default=0)
    payment = models.CharField(max_length=4, choices=PAYMENT, default='PSPD')

    def __str__(self):
        prod_list = [prod.name for prod in self.products.all()]
        return self.name + " : " + ",".join(prod_list)



class CartTemplate(models.Model):
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    help_text = models.CharField(max_length=200, default='help text for cart template', unique=False)
    products = models.ManyToManyField(Product)

    def __str__(self):
        prod_list = [prod.name for prod in self.products.all()]
        return self.name + " : " + ",".join(prod_list)
