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
        return self.name
   
class Order(models.Model):
    customer = models.ForeignKey("Customer",null= True,on_delete=models.SET_NULL)
    date_orderd = models.DateTimeField(auto_now=True)
    transaction_id = models.IntegerField(null=True)


    




class Order_item(models.Model):
    product= models.ForeignKey("Product",null=True,on_delete=models.SET_NULL)
    order = models.ForeignKey("Order",null= True,on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now=True)

      