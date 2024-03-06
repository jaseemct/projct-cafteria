from django.db import models


# Create your models here.
class product(models.Model):
     product_id=models.CharField(max_length=100)
     product_name=models.CharField(max_length=100)
     image=models.ImageField(upload_to='product')
     description=models.CharField(max_length=300)
     price=models.IntegerField()
     category=models.CharField(max_length=1300,default='')
     
class CartModle(models.Model):
     # user=models.ForeignKey()
     total=models.IntegerField(default=0)
     
class Lineitems(models.Model):
     cart=models.ForeignKey(CartModle,on_delete=models.CASCADE)
     product=models.ForeignKey(product,on_delete=models.CASCADE)
     quntity=models.IntegerField(default=0)
     total=models.IntegerField(default=0)
     
class order(models.Model):
     user_name=models.CharField(max_length=100)
     first_name=models.CharField(max_length=100)
     last_name=models.CharField(max_length=100)
     country=models.CharField(max_length=100)
     address=models.CharField(max_length=100)
     email=models.CharField(max_length=100)
     payment_id=models.CharField(max_length=100)
     provider_order_id=models.CharField(max_length=100,default='')
     signature_id=models.CharField(max_length=100,default='')
     products=models.CharField(max_length=100)
     total_amount=models.CharField(max_length=100)
     date=models.CharField(max_length=100)
     status=models.CharField(max_length=1)
     phone=models.CharField(max_length=100,default='')     