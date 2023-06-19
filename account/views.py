from django.shortcuts import get_object_or_404, render,redirect

from order.models import Order, OrderProduct
from .forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .models import Account, Otp, UserProfile
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from cart.models import Cart,CartItem
import math,random

# Create your views here.
def register(request):
  if request.user.is_authenticated:
    # User is already authenticated, redirect to previous page using Referer header
    referer = request.META.get('HTTP_REFERER')
    if referer:
      messages.info(request, f'{request.user.username} you are already login')
      return redirect(referer)

  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    email=request.POST['email']
    if form.is_valid():
      user=form.save(commit=False)
      user.username=email.split('@')[0]
      user.save()

      #Account verification
      current_site=get_current_site(request)
      mail_subject='Please activate your account'
      message=render_to_string('account/account_verification_email.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
      })
      to_email=email
      sent_email=EmailMessage(mail_subject,message,to=[to_email,])
      sent_email.send()
      return redirect(f'/account/login/?command=verification&email={email}')
    else:
      messages.error(request,'Please fill the form properly!')  
      return redirect('register')
  else:
    form = RegistrationForm()
  context={
    'form':form
  }    
  return render(request,'account/register.html', context)

def activate(request,uidb64,token):
  try:
    uid=urlsafe_base64_decode(uidb64).decode()
    user=Account.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user=None
  if user is not None and default_token_generator.check_token(user, token):
    user.is_active=True
    user.save()
    userProfile=UserProfile()
    userProfile.user=user
    userProfile.save()
    messages.success(request,'Congratulation! your account is activated')
    return redirect('login')
  else:
    messages.error(request,'Invalid activation link!')
    return redirect('register')   

def generate_otp():
  orcus="0123456789"
  size=6
  length=len(orcus)
  otp=""
  for i in range(size):
    otp+=orcus[math.floor(random.random()*length)]
  return otp  

def send_otp(email, otp):
  subject = 'OTP Verification'
  message = f'Your OTP is: {otp}'
  to_email=email
  EmailMessage(subject, message,to_email,to=[to_email,]).send()

def user_login(request):
  if request.method == "POST":
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is not None:
      # Generate OTP and send it to the user's email address
      otp = generate_otp()
      send_otp(email, otp)
      # Save OTP in the database
      otp_instance = Otp(user=user, otp=otp)
      otp_instance.save()  
      request.session['user_id'] = user.id 
      # Redirect to OTP verification page
      return redirect('otp')
    else:
      messages.error(request, 'Invalid login credentials')
      return redirect('login')
  return render(request, 'account/login.html')

def otp_verify(request):
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        user_id = request.session.get('user_id')
        try:
            user = Account.objects.get(id=user_id)
            otp_instance = Otp.objects.get(user=user)
            if otp_instance.otp == int(otp_entered):
                otp_instance.delete()

                # Check if a non-user cart exists
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                except Cart.DoesNotExist:
                    cart = None

                if cart is not None:
                    # Merge the non-user cart items with the logged-in user's cart
                    cart_items = CartItem.objects.filter(cart=cart)
                    for item in cart_items:
                        product = item.product
                        variations = item.variations.all()

                        if variations:
                            user_cart = CartItem.objects.filter(product=product, user=user, variations__in=variations).first()
                        else:
                            user_cart = CartItem.objects.filter(product=product, user=user, variations__isnull=True).first()

                        if user_cart:
                            user_cart.quantity += item.quantity
                            user_cart.save()
                        else:
                            item.user = user
                            item.cart = None
                            item.save()

                    cart_items.delete()

                login(request, user)
                messages.success(request, f'{user.username} logged in successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid OTP')
                return redirect('otp')
        except Account.DoesNotExist:
            messages.error(request, 'User not found')
        except Otp.DoesNotExist:
            messages.error(request, 'OTP verification failed')
    return render(request, 'account/otp.html')



@login_required(login_url='login')
def user_logout(request):
  username=request.user.username
  logout(request)
  messages.success(request,f'{username} you are logged out successfully!')
  return redirect('home')

def forgot_password(request):
  if request.method == "POST":
    email=request.POST['email']
    if Account.objects.filter(email=email).exists():
      user=Account.objects.get(email__exact=email)

      current_site=get_current_site(request)
      mail_subject='Reset Your Password'
      message=render_to_string('account/reset_password_validation.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
      })
      to_email=email
      sent_email=EmailMessage(mail_subject,message,to=[to_email,])
      sent_email.send()
      return redirect(f'/account/login/?command=validation&email={email}')
    else:
      messages.error(request,"User does not exist!")
      return redirect('forgot_password')

  return render(request,'account/forgot_password.html')  

def reset_password_validation(request,uidb64,token):
  try:
    uid=urlsafe_base64_decode(uidb64).decode()
    user=Account.objects.get(pk=uid)
  except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user=None
  if user is not None and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    messages.success(request,'Please reset your password!')
    return redirect('reset_password')
  else:
    messages.error(request,'This link has been expired!')  
    return redirect('forgot_password')

def reset_password(request):
  if request.method == "POST":
    password1=request.POST['password1']
    password2=request.POST['password2']
    if password1 == password2:
      uid=request.session.get('uid')
      user=Account.objects.get(pk=uid)
      user.set_password(password1)
      user.save()
      messages.success(request,'Password reseted successfully!')
      return redirect('login')
    else:
      messages.error(request,'Password does not match!')
      return redirect('reset_password')
  else:
    return render(request,'account/reset_password.html')

@login_required(login_url='login')
def dashboard(request):
  orders=Order.objects.filter(user_id=request.user.id,is_ordered=True).order_by('-created_at')
  order_count=orders.count()
  user_profile=UserProfile.objects.get(user_id=request.user.id)
  context={
    'order_count':order_count,
    'user_profile':user_profile
  }
  return render(request,'account/dashboard.html',context)

@login_required(login_url='login')
def my_orders(request):
  orders=Order.objects.filter(user_id=request.user.id,is_ordered=True).order_by('-created_at')
  context={
    'orders':orders,
  }
  return render(request,'account/my_orders.html',context) 

@login_required(login_url='login')
def order_detail(request,order_id):
  order_detail=OrderProduct.objects.filter(order__order_number=order_id)
  order=Order.objects.get(order_number=order_id)
  subtotal=0
  for i in order_detail:
    subtotal += i.product_price * i.quantity
  context={
    'order_detail':order_detail,
    'order':order,
    'subtotal':subtotal,
  }  
  return render(request,'account/order_detail.html',context) 

@login_required(login_url='login')
def edit_profile(request):
  userprofile=get_object_or_404(UserProfile,user=request.user)
  if request.method=="POST":
    user_form=UserForm(request.POST,instance=request.user)
    profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, 'Your profile has been updated')
      return redirect('edit_profile')
  else:
    user_form=UserForm(instance=request.user)
    profile_form=UserProfileForm(instance=userprofile) 
  context={
    'user_form':user_form,
    'profile_form':profile_form,
    'userprofile':userprofile,
  }
  return render(request,'account/edit_profile.html',context)

@login_required(login_url='login')
def change_password(request):
  if request.method=="POST":
    current_password=request.POST.get('current_password')
    new_password=request.POST.get('new_password')
    confirm_password=request.POST.get('confirm_password')
    user=Account.objects.get(username__exact=request.user.username)
    if new_password == confirm_password:
      success=user.check_password(current_password)
      if success:
        user.set_password(new_password)
        user.save()
        messages.success(request,'Your password updated successfully')
        return redirect('change_password')
      else:
        messages.error(request, 'Please enter valid current password') 
        return redirect('change_password')
    else:
      messages.error(request, 'Password Does Not Match') 
      return redirect('change_password')   
  return render(request,'account/change_password.html')

def OrderTrack(request, id):
    order_tracking = None
    try:
        order_tracking = Order.objects.get(id=id)
    except:
        Order.DoesNotExist

    order_processing = order_tracking.status
    context = {
        'order_tracking' : order_tracking,
        'order_processing' : order_processing,
    }

    return render(request,'account/order_tracking.html', context)