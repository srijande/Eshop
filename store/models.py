from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from cloudinary.models import CloudinaryField

class Customer(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True , blank=True)
    name= models.CharField(max_length=200, null=True, blank=True)
    email= models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    name= models.CharField(max_length=200, null=True, blank=True)
    price= models.DecimalField(max_digits=7, decimal_places=2)
    image=CloudinaryField(null=True, blank=True)

    def __str__(self):
       return self.name

    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
            

class Order(models.Model):
    transaction_id= models.CharField(max_length=200, null=True)
    customer= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    complete= models.BooleanField(default=False,null=True,blank=False)
    date_ordered= models.DateTimeField(auto_now_add=True)



    def __str__(self):
       return str(self.transaction_id)
        
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity*item.product.price for item in orderitems])
        return total
        
    @property
    def get_cart_items(self):
        orderitems= self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added= models.DateTimeField(auto_now_add=True)
    
 
    def get_total(self):
        total=self.product.price*self.quantity
        return int(total)



# class ShippingAddress(models.Model):
#     order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
#     customer= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
#     address= models.CharField(max_length=200, null=True, blank=True)
#     city= models.CharField(max_length=200, null=True, blank=True)
#     state= models.CharField(max_length=200, null=True, blank=True)
#     pincode= models.CharField(max_length=200, null=True, blank=True)
#     date_added= models.DateTimeField(auto_now_add=True,blank=True)
    
#     def __str__(self):
#        return self.address





  
