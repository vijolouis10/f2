from django.db import models
from account.models import Account
from store.models import Product,Variation

# Create your models here.
class Payment(models.Model):
  user=models.ForeignKey(Account, on_delete=models.CASCADE)
  payment_id=models.CharField(max_length=100)
  payment_method=models.CharField(max_length=100)
  amount_paid=models.CharField(max_length=100)
  status=models.CharField(max_length=100)
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.payment_id

class Order(models.Model):
  STATUS = (
    ('Processing','Processing'),
    ('Accepted','Accepted'),
    ('Out For Delivery','Out For Delivery'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
    ) 
  user=models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)  
  payment=models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True) 
  order_number=models.CharField(max_length=20)
  first_name=models.CharField(max_length=50)
  last_name=models.CharField(max_length=50)
  phone_number=models.CharField(max_length=12)
  email=models.EmailField(max_length=50)
  address_line_1=models.CharField(max_length=50)
  address_line_2=models.CharField(max_length=50,blank=True)
  city=models.CharField(max_length=50)
  pincode=models.CharField(null=True,max_length=6)
  state=models.CharField(max_length=50)
  country=models.CharField(max_length=50)
  order_note=models.CharField(max_length=100,blank=True)
  order_total=models.FloatField()
  status=models.CharField(max_length=16,choices=STATUS,default='Processing')
  ip=models.CharField(blank=True,max_length=20)
  is_ordered=models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.first_name

  def full_name(self):
    return self.first_name +" "+ self.last_name  

  def full_address(self):
    return self.address_line_1 +", "+self.address_line_2    

class OrderProduct(models.Model):
  order=models.ForeignKey(Order, on_delete=models.CASCADE)
  payment=models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True,null=True)
  user=models.ForeignKey(Account, on_delete=models.CASCADE)
  product=models.ForeignKey(Product, on_delete=models.CASCADE)
  variations = models.ManyToManyField(Variation, blank=True)
  quantity=models.IntegerField()
  product_price=models.FloatField()
  ordered=models.BooleanField(default=False)
  craeted_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  def sub_total(self):
     return self.quantity * self.product_price

  def __str__(self):
      return self.product.name
  
