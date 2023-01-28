from django.db import models
from users.models import User


# Create your models here.
class Product(models.Model):
    Product_name = models.CharField(max_length=30)
    Price = models.IntegerField ()
    Rating = models.CharField(max_length=5)
    Review = models.CharField(max_length= 200)
    photo = models.ImageField(upload_to = 'pics')
    
 



class Customer(models.Model):
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   name = models.CharField(max_length= 80)

   def __str__(self):
        return self.user.email
   
class Order(models.Model):
    customer = models.ForeignKey(Customer,null= True,on_delete=models.SET_NULL)
    date_orderd = models.DateTimeField(auto_now=True)
    transaction_id = models.IntegerField(null=True)
    complete= models.BooleanField(null=True)

    @property
    def get_cart_total(self):
        orderitems = self.order_item_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total    


  


class Order_item(models.Model):
    product= models.ForeignKey("Product",null=True,on_delete=models.SET_NULL)
    order = models.ForeignKey("Order",null= True,on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):        
        total = self.quantity*self.product.Price
        return total

      