from .models import AppliedCoupon, Coupon, Wishlist,Cart,CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from store.models import Product,Variation
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


@login_required(login_url='login')
def wishlist(request):
  wishlist=Wishlist.objects.filter(user=request.user)
  context={
    'wishlist':wishlist,
  }
  return render(request,'cart/wishlist.html',context)

def add_wishlist(request):
  if request.method == "POST":
    id=int(request.POST['item_id'])
    product=Product.objects.get(id=id)
    if (product):
      if (Wishlist.objects.filter(user=request.user, products=product)):
        return JsonResponse({'status':"Product already exist in wishlist"})
      else:
        Wishlist.objects.create(user=request.user, products=product)
        return JsonResponse({'status':"Product added to wishlist"})
    else:
       return JsonResponse({'status':"No such product found in wishlist"})

def remove_wishlist(request):
  if request.method == "POST":
    id=int(request.POST['item_id'])
    product=Product.objects.get(id=id)
    if (product):
      if (Wishlist.objects.filter(user=request.user, products=product)):
        Wishlist.objects.get(user=request.user, products=product).delete()
        return JsonResponse({'status':"Product remove from wishlist"})
      else:
        return JsonResponse({'status':"Product does not found in wishlist"})
    else:
      return JsonResponse({'status':"No such product found"})

def wishlist_count(request):
  if request.user.is_authenticated:
    wishCount = Wishlist.objects.filter(user=request.user).count()
    return JsonResponse({'wishCount': wishCount})
  else:
    return JsonResponse({'wishCount': 0})       


def cart(request,total=0,quantity=0,cart_items=None):
  coupon = None
  if 'coupon' in request.session:
      coupon = request.session['coupon']
      x = Coupon.objects.get(coupon=coupon)
      discount = x.discount
  else:
      discount = 0
  try:
    tax=0
    grand_total=0
    if request.user.is_authenticated:
      cart_items=CartItem.objects.filter(user=request.user).order_by('product_id')
    else:
      cart=Cart.objects.get(cart_id=_cart_id(request))
      cart_items=CartItem.objects.filter(cart=cart,is_available=True).order_by('product_id')
    for cart_item in cart_items:
      total +=(cart_item.product.selling_price * cart_item.quantity)
      quantity += cart_item.quantity
    grand_total=total - discount
  except ObjectDoesNotExist:
    pass    
  context={
    'cart_items':cart_items,
    'total':total,
    'quantity':quantity,
    'discount':discount,
    'grand_total':grand_total,
    'coupon':coupon,
  }
  return render(request,'cart/cart.html',context)

def coupon_apply(request):
  if request.method == 'POST':
    coupon = request.POST.get('coupon')
    try:
      if Coupon.objects.get(coupon=coupon, is_active=True):
        applied_coupon = Coupon.objects.get(coupon=coupon, is_active=True)
        try:
          if AppliedCoupon.objects.get(user=request.user,coupon=applied_coupon):
            messages.error(request, 'Coupon has expired!')
            return redirect('cart')
        except:
          request.session['coupon'] = coupon 
          messages.success(request, 'Coupon Applied Successfully')
      else:
        messages.error(request, 'Invalid Coupon!')
        return redirect('cart')

    except:
      Coupon.DoesNotExist
      messages.error(request, 'Invalid Coupon')

  return redirect('cart')

def remove_coupon(request):
    del request.session['coupon']
    return redirect('cart')

def _cart_id(request):
  cart=request.session.session_key
  if not cart:
    cart=request.session.create()
  return cart  


def add_cart(request):
    product_variation=[]
    if request.method == "POST":
      id=int(request.POST['item_id'])
      product=Product.objects.get(id=id)
      quantity=int(request.POST['quantity'])
      size=request.POST['size']
      try:
          variation=Variation.objects.get(product=product,size__iexact=size)
          product_variation.append(variation)
      except:
          pass

    if request.user.is_authenticated:
        is_cart_exists=CartItem.objects.filter(product=product,user=request.user).exists()
        if is_cart_exists:
            cart_item=CartItem.objects.filter(product=product,user=request.user)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                if (item.quantity + quantity) <= product.stock:
                  item.quantity += quantity
                  item.save()
                else:
                  return JsonResponse({'status':f"Only {product.stock} quantity availabe this product"})  
            else:
                if quantity <= product.stock:
                  item=CartItem.objects.create(product=product,quantity=quantity,user=request.user)
                  if len(product_variation) > 0:
                      item.variations.clear()
                      item.variations.add(*product_variation) 
                  item.save()
                else:
                  return JsonResponse({'status':f"Only {product.stock} quantity availabe this product"})    
        else:
            if quantity <= product.stock:
              cart_item=CartItem.objects.create(product=product,quantity=quantity,user=request.user)
              if len(product_variation) > 0:
                  cart_item.variations.clear()
                  cart_item.variations.add(*product_variation)
              cart_item.save() 
            else:
              return JsonResponse({'status':f"Only {product.stock} quantity availabe this product"})   
    else:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()  
        is_cart_exists=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                if (item.quantity + quantity) <= product.stock:
                  item.quantity += quantity
                  item.save()
                else:
                  return JsonResponse({'status':f"Only {product.stock} quantity availabe this product"})
            else:
                if quantity <= product.stock:
                  item=CartItem.objects.create(product=product,quantity=quantity,cart=cart)
                  if len(product_variation) > 0:
                      item.variations.clear()
                      item.variations.add(*product_variation) 
                  item.save()
                else:
                  return JsonResponse({'status':f"Only {product.stock} quantity availabe this product"}) 
        else:
            if quantity <= product.stock:
              cart_item=CartItem.objects.create(product=product,quantity=quantity,cart=cart)
              if len(product_variation) > 0:
                  cart_item.variations.clear()
                  cart_item.variations.add(*product_variation)
              cart_item.save()  
            else:
               return JsonResponse({'status':f"Only {product.stock} quantity availabe this product"})   
    return JsonResponse({'status':"Product added to cart"})


def cart_count(request):
  cartCount=0
  cart=Cart.objects.filter(cart_id=_cart_id(request)) 
  if request.user.is_authenticated:
    cart_items=CartItem.objects.filter(user=request.user) 
  else:   
    cart_items=CartItem.objects.filter(cart=cart[:1]) 
  for cart_item in cart_items:
    cartCount += cart_item.quantity
  return JsonResponse({'cartCount':cartCount})  

def remove_cart(request):
  if request.method=="POST":
    id=int(request.POST['item_id'])
    product=Product.objects.get(id=id)
    cart_id=int(request.POST['cart_id'])
    if request.user.is_authenticated:
      cart_item=CartItem.objects.get(user=request.user,product=product,id=cart_id)
    else:
      cart=Cart.objects.get(cart_id=_cart_id(request))
      cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_id) 
    cart_item.delete()
    return JsonResponse({'status':'Cart item removed from cart'})  

def decrease_quantity(request):
  if request.method=="POST":
    id=int(request.POST['item_id'])
    product=Product.objects.get(id=id)
    cart_id=int(request.POST['cart_id'])
    if request.user.is_authenticated:
      cart_item=CartItem.objects.get(user=request.user,product=product,id=cart_id)
      if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
      else:
        cart_item.delete()  
    else:
      cart=Cart.objects.get(cart_id=_cart_id(request))
      cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_id) 
      if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
      else:
        cart_item.delete()  
    return JsonResponse({'status':'Product updated to cart Item'})  

def increase_quantity(request):
  if request.method=="POST":
    id=int(request.POST['item_id'])
    product=Product.objects.get(id=id)
    cart_id=int(request.POST['cart_id'])
    if request.user.is_authenticated:
      cart_item=CartItem.objects.get(user=request.user,product=product,id=cart_id)
      if cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()
      else:
        return JsonResponse({'status':f"Only {product.stock} quantity available this product"}) 
    else:
      cart=Cart.objects.get(cart_id=_cart_id(request))
      cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_id) 
      if cart_item.quantity < product.stock:
        cart_item.quantity += 1
        cart_item.save()
      else:
        return JsonResponse({'status':f"Only {product.stock} quantity available this product"}) 
    return JsonResponse({'status':'Product updated to cart Item'})      

@login_required(login_url='login')
def checkout(request, cart_items=None, total=0, quantity=0):
    grand_total=0
    try:
        if request.user.is_authenticated:  
            if 'coupon' in request.session:
                coupon = request.session['coupon']
                x = Coupon.objects.get(coupon=coupon)
                discount = x.discount
            else:
                discount = 0

            cart_items=CartItem.objects.filter(user=request.user, is_available=True)
            if cart_items.count() <= 0:
                return redirect('store') 
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart, is_available=True)
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.quantity) 
            quantity += cart_item.quantity
        grand_total = total - discount
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'discount':discount,
        'grand_total':grand_total
    }
    return render(request, 'cart/checkout.html', context)