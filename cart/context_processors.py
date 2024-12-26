from .models import Wishlist
from .models import Cart,CartItem
from .views import _cart_id

def wishlist_count(request):
  if request.user.is_authenticated:
    wishCount=Wishlist.objects.filter(user=request.user).count()
  else:
    wishCount=0
  return dict(wishCount=wishCount)  

def cart_count(request):
  cartCount=0
  if 'admin' in request.path:
    return {}
  else:
    try:
      cart=Cart.objects.filter(cart_id=_cart_id(request)) 
      if request.user.is_authenticated:
        cart_items=CartItem.objects.filter(user=request.user) 
      else:   
        cart_items=CartItem.objects.filter(cart=cart[:1]) 
      for cart_item in cart_items:
        cartCount += cart_item.quantity
    except:
      cartCount=0
  return dict(cartCount=cartCount)        
