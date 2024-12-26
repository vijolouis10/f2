from django.db import models
from account.models import Account
from store.models import Product, Variation


class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)

    
class Cart(models.Model):
  cart_id=models.CharField(max_length=2500, blank=True)
  date_added=models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return self.cart_id

class CartItem(models.Model):
  user=models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
  product=models.ForeignKey(Product, on_delete=models.CASCADE)  
  variations=models.ManyToManyField(Variation,blank=True)  
  cart=models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)  
  quantity=models.IntegerField()
  is_available=models.BooleanField(default=True)

  def sub_total(self):
    return self.product.selling_price * self.quantity

  def __str__(self):
      return self.product.name

class Coupon(models.Model):
    coupon      = models.CharField(max_length=20, null=True)
    discount    = models.IntegerField(null=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon

class AppliedCoupon(models.Model):
    user        = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)  
    coupon      = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.coupon.coupon