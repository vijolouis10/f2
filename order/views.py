from django.shortcuts import render,redirect
from cart.models import AppliedCoupon, CartItem, Coupon
from . models import Order,Payment,OrderProduct
import datetime
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

def payments(request):
  body = json.loads(request.body)
  order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
  payment = Payment(
    user = request.user,
    payment_id = body['transID'],
    payment_method = body['payment_method'],
    amount_paid = order.order_total,
    status = "Processing"
    )
  payment.save()
  order.payment = payment
  order.is_ordered = True
  order.save()

  cart_items=CartItem.objects.filter(user=request.user)
  for item in cart_items:
    orderproduct=OrderProduct()
    orderproduct.order_id=order.id
    orderproduct.payment=payment
    orderproduct.user_id=request.user.id
    orderproduct.product_id=item.product.id
    orderproduct.quantity=item.quantity
    orderproduct.product_price=item.product.selling_price
    orderproduct.ordered=True
    orderproduct.save()

    cart_item=CartItem.objects.get(id=item.id)
    product_variation=cart_item.variations.all()
    orderproduct=OrderProduct.objects.get(id=orderproduct.id)
    orderproduct.variations.set(product_variation)
    orderproduct.save()

    product=Product.objects.get(id=item.product_id)
    product.stock -= item.quantity
    product.save()
  CartItem.objects.filter(user=request.user).delete() 

  if 'coupon' in request.session:
    try:
      coupon = request.session['coupon']
      coupon_applied = Coupon.objects.get(coupon=coupon)
      x = AppliedCoupon.objects.create(user=request.user,coupon=coupon_applied)
      x.save()
      del request.session['coupon']
    except:
      pass

  mail_subject='Thank you for your order!'
  message=render_to_string('order/order_recieved_email.html',{
    'user':request.user,
    'order':order,
  })
  to_email=request.user.email
  sent_email=EmailMessage(mail_subject,message,to=[to_email,])
  sent_email.send()

  data={
    'order_number':order.order_number,
    'transID':payment.payment_id,
  }
  return JsonResponse(data)

# Create your views here.
def place_order(request,total=0):
  current_user=request.user
  cart_items=CartItem.objects.filter(user=current_user)
  cart_count=cart_items.count()
  if cart_count <= 0:
    return redirect('store')
  
  coupon = None
  if 'coupon' in request.session:
      coupon = request.session['coupon']
      x = Coupon.objects.get(coupon=coupon)
      discount = x.discount
  else:
      discount = 0

  grand_total=0
  for cart_item in cart_items:
    total +=(cart_item.product.selling_price*cart_item.quantity)
  grand_total=total-discount  
  if request.method == "POST":
      data=Order()
      data.user=current_user
      data.first_name=request.POST['first_name']
      data.last_name=request.POST['last_name']
      data.phone_number=request.POST['phone_number']
      data.email=request.POST['email']
      data.address_line_1=request.POST['address_line_1']
      data.address_line_2=request.POST['address_line_2']
      data.city=request.POST['city']
      data.pincode=request.POST['pincode']
      data.state=request.POST['state']
      data.country=request.POST['country']
      data.order_note=request.POST['order_note']
      data.order_total=grand_total
      data.ip=request.META.get('REMOTE_ADDR')
      data.save()
      yr=int(datetime.date.today().strftime('%Y'))
      mt=int(datetime.date.today().strftime('%m'))
      dt=int(datetime.date.today().strftime('%d'))
      d=datetime.date(yr,mt,dt)
      current_date=d.strftime('%Y%m%d')
      order_number=current_date +str(data.id)
      data.order_number=order_number
      data.save()
      
      order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
      context={
        'order':order,
        'cart_items':cart_items,
        'total':total,
        'grand_total':grand_total,
        'discount':discount,
      }
      return render(request,'order/payment.html',context)
  else:
      return redirect('checkout')

def order_complete(request):
  order_number = request.GET.get('order_number')
  transID = request.GET.get('payment_id')
  try:
    order = Order.objects.get(order_number=order_number, is_ordered=True)
    payment = Payment.objects.get(payment_id=transID)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    

    subtotal = 0
    for item in ordered_products:
      subtotal += item.product_price * item.quantity

    disc=  subtotal-order.order_total

    context = {
      'order': order,
      'ordered_products': ordered_products,
      'order_number': order.order_number,
      'transID': payment.payment_id,
      'payment': payment,
      'subtotal': subtotal,
      'disc':disc,
    }
    return render(request, 'order/order_complete.html', context)
  except (Payment.DoesNotExist, Order.DoesNotExist):
    return redirect('home')





