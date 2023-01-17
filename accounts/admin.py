from django.contrib import admin

from accounts.models import Product, Order, Customer,  Order_item


# Register your models here.


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Order_item)