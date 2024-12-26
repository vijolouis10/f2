from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
import datetime
import csv
import xlwt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate,login,logout
from order.models import Payment, OrderProduct, Order
from store.models import Product,Category,PhotoGallary,Variation
from cart.models import Coupon
from account.models import Account


# Create your views here.

def AdminLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_superadmin:
                login(request,user)
                return redirect('adminhome')
            else:
                messages.error(request,"Invalid Credentials")
                return redirect('admin_login')
        else:
            messages.error(request,"Invalid Credentials")
    
    return render(request, 'my_admin/admin_login.html')

def AdminLogout(request):
    logout(request)
    return redirect('admin_login')

@login_required(login_url='admin_login')
def AdminHome(request):
    if not request.user.is_superadmin:
        return redirect('home')
    
    paypal_total = 0
    total_earning = 0
    sold_products = 0
    paypal = Payment.objects.filter(payment_method='PayPal')
    for i in paypal:
        paypal_total += float(i.amount_paid)

  

    total = Payment.objects.all()
    for i in total:
        total_earning += float(i.amount_paid)

    sold_products = OrderProduct.objects.all().count()
    orders = Order.objects.filter(is_ordered=True).order_by('-id')[:10]

    processing = OrderProduct.objects.filter(order__status='Processing').count()
    accepted = OrderProduct.objects.filter(order__status='Accepted').count()
    out_delivery = OrderProduct.objects.filter(order__status='Out For Delivery').count()
    delivered = OrderProduct.objects.filter(order__status='Delivered').count()
    cancelled = OrderProduct.objects.filter(order__status='Cancelled').count()



    context = {
        'paypal_total' : paypal_total,
        'total_earning' : total_earning,
        'sales' : sold_products,
        'orders' : orders,
        'processing' : processing,
        'accepted' : accepted,
        'out_delivery' : out_delivery,
        'delivered':delivered,
        'cancelled' : cancelled,
    }
    
    return render(request, 'my_admin/admin_home.html', context)

@login_required(login_url='admin_login')
def UsersTable(request):
    if not request.user.is_superadmin:
        return redirect('home')
    
    users = Account.objects.all()
    context = {
        'users' : users,
    }

    return render(request, 'my_admin/users_table.html', context)

def BlockUser(request,id):
    user = Account.objects.get(id=id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()

    return redirect(UsersTable)

@login_required(login_url='admin_login')
def ProductTable(request):
    if not request.user.is_superadmin:
        return redirect('home')

    products = Product.objects.all().order_by('created_date')
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)  # returns the desired page object
    context = {
        'products' : page_products,
    }

    return render(request, 'my_admin/product_table.html', context)

@login_required(login_url='admin_login')
def product_gallery(request):
    if not request.user.is_superadmin:
        return redirect('home')

    products = PhotoGallary.objects.all().order_by('product')
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)  # returns the desired page object
    context = {
        'products' : page_products,
    }

    return render(request, 'my_admin/product_gallary.html', context)

@login_required(login_url='admin_login')
def product_variation(request):
    if not request.user.is_superadmin:
        return redirect('home')

    products = Variation.objects.all().order_by('product')
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_products = paginator.get_page(page_number)  # returns the desired page object
    context = {
        'products' : page_products,
    }

    return render(request, 'my_admin/product_variation.html', context)

@login_required(login_url='admin_login')
def AddVaraiation(request):
    products = Product.objects.all()
    if request.method == 'POST':
        product = request.POST.get('product')
        size=request.POST.get('size')

        if product == "" or size == "":
            messages.error(request, "All Fields Are Required")
        else:
            variation = Variation(size=size)
            variation.product = Product.objects.get(id=product)
            variation.save()
            return redirect('product_variation')

    context = {
        'products' :products,
    }

    return render(request, 'my_admin/add_variation.html', context)

@login_required(login_url='admin_login')
def VariationStatus(request, id):
    variation = Variation.objects.get(id=id)
    if variation.is_active:
        variation.is_active = False
    else:
        variation.is_active = True
    variation.save()
    return redirect('product_variation')

@login_required(login_url='admin_login')
def VariationDelete(request, id):
    variation = Variation.objects.get(id=id)
    variation.delete()
    return redirect('product_variation')


@login_required(login_url='admin_login')
def EditProduct(request,id):
    product = Product.objects.get(id=id)
    categories = Category.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        if product_name == "" or description == "" or price == "" or stock == "" or image == "":
            messages.error(request, "All Fields Are Required")
        else:
            product_obj = Product.objects.get(id=id)
            product_obj.name = product_name
            product_obj.description = description
            product_obj.selling_price = price
            product_obj.stock = stock
            product_obj.slug = slugify(product_name)
            if image:
                product_obj.image = image 
            else:
                pass 
            product_obj.save()
            return redirect('product_table')

    context = {
        'product' : product,
        'categories' : categories,
    }
    return render(request, 'my_admin/edit_product.html', context)

@login_required(login_url='admin_login')
def AddProduct(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if product_name == "" or description == "" or price == "" or stock == "" or image == "" or category == "":
            messages.error(request, "All Fields Are Required")
        else:
            product = Product(
                name = product_name, description = description, selling_price = price, stock = stock, image = image
            )
            product.category = Category.objects.get(id=category)
            product.slug = slugify(product_name)
            product.save()
            return redirect('product_table')

    context = {
        'categories' : categories,
    }

    return render(request, 'my_admin/add_product.html', context)

@login_required(login_url='admin_login')
def add_gallery(request):
    products = Product.objects.all()
    if request.method == 'POST':
        product = request.POST.get('product')
        image = request.FILES.get('image')

        if product == "" or image == "" :
            messages.error(request, "All Fields Are Required")
        else:
            photo = PhotoGallary(image = image,)
            photo.product = Product.objects.get(id=product)
            photo.save()
            return redirect('product_gallery')

    context = {
        'products' : products,
    }

    return render(request, 'my_admin/add_gallery.html', context)

@login_required(login_url='admin_login')
def DeleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('product_table')

@login_required(login_url='admin_login')
def DeleteGallery(request, id):
    product = PhotoGallary.objects.get(id=id)
    product.delete()
    return redirect('product_gallery')

@login_required(login_url='admin_login')
def CategoryTable(request):
    if not request.user.is_superadmin:
        return redirect('home')

    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }
    return render(request, 'my_admin/category_table.html', context)

@login_required(login_url='admin_login')
def EditCategory(request,id):
    category = Category.objects.get(id=id)

    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if category_name == "" or description == "" or image == "":
            messages.error(request, "All Fields Are Required")
        else:
            category_obj = Category.objects.get(id=id)
            category_obj.name = category_name
            category_obj.description = description
            category_obj.slug = slugify(category_name)
            if image:
                category_obj.image = image 
            else:
                pass 
            category_obj.save()
            return redirect('category_table')

    context = {
        'category' : category,
    }
    return render(request, 'my_admin/edit_category.html', context)

@login_required(login_url='admin_login')
def AddCategory(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if category_name == "" or description == "" or image == "":
            messages.error(request, "All Fields Are Required")
        else:
            category = Category(
                name = category_name, description = description, image = image
            )
            category.slug = slugify(category_name)
            category.save()
            return redirect('category_table')

    return render(request, 'my_admin/add_category.html')

@login_required(login_url='admin_login')
def DeleteCategory(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('category_table')

@login_required(login_url='admin_login')
def OrderTable(request):
    if not request.user.is_superadmin:
        return redirect('home')

    orders = Order.objects.filter(is_ordered=True).order_by('-created_at')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_orders = paginator.get_page(page_number)  # returns the desired page object
    context = {
        'orders' : page_orders
    }

    return render(request, 'my_admin/order_table.html', context)

@login_required(login_url='admin_login')
def ViewOrder(request, id):
  order = Order.objects.get(id=id)
  order_products = OrderProduct.objects.filter(order=order)
  context = {
      'order_products' : order_products,
    }
  return render(request, 'my_admin/view_order.html', context)

@login_required(login_url='admin_login')
def OrderStatus(request, id):
    order = Order.objects.get(id=id)
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        status = request.POST.get('status')
        order.status = status
        order.save()
    return redirect(url)




# @login_required(login_url='admin_login')
# def OrderStatus(request, id):
#     url = request.META.get('HTTP_REFERER')
#     order_product = OrderProduct.objects.get(id=id)
#     if request.method == "POST":
#         status = request.POST.get('status')
#         order_product.status = status
#         order_product.save()
#         if OrderTracking.objects.filter(order_id = order_product.id).exists():
#             order_tracking = OrderTracking.objects.get(order_id = order_product.id)
#         else:
#             order_tracking = OrderTracking(order_id = order_product.id)
#         if status == 'Accepted':  
#             order_tracking.accepted = status
#             order_tracking.a_date = timezone.now()
#             order_tracking.save()
#         elif status == 'Out For Delivery':
#             order_tracking.out_delivery= status
#             order_tracking.out_date = timezone.now()
#             order_tracking.save()
#         elif status == 'Delivered':
#             order_tracking.delivered = status
#             order_tracking.d_date = timezone.now()
#             order_tracking.save()   
#         elif status == 'Cancelled':
#             order_tracking.cancelled = status
#             order_tracking.c_date = timezone.now()
#             order_tracking.save() 

#     return redirect(url)

# @login_required(login_url='admin_login')
# def BannerTable(request):
#     if not request.user.is_superadmin:
#         return redirect('home')

#     banners = Banner.objects.all()
#     return render(request, 'my_admin/banner_table.html', {'banners':banners})

# @login_required(login_url='admin_login')
# def AddBanner(request):
#     if request.method == 'POST':
#         image = request.FILES.get('banner')
#         banner = Banner(banner=image)
#         banner.save()
#         return redirect('banner_table')

#     return render(request, 'my_admin/add_banner.html')

# @login_required(login_url='admin_login')
# def EditBanner(request, id):
#     url = request.META.get('HTTP_REFERER')
#     banner = Banner.objects.get(id=id)
#     if request.method == 'POST':
#         status = request.POST.get('status')
#         if status == 'Live':
#             banner.is_live = True
#         else:
#             banner.is_live = False
#         banner.save()
#     return redirect(url)

# @login_required(login_url='admin_login')
# def DeleteBanner(request, id):
#     banner = Banner.objects.get(id=id)
#     banner.delete()
#     return redirect('banner_table')

@login_required(login_url='admin_login')
def SalesTable(request):
    if not request.user.is_superadmin:
        return redirect('home')

    orders = Order.objects.filter(is_ordered=True).order_by('-id')
    context = {
        'orders' : orders
    }

    return render(request, 'my_admin/sales_table.html', context)

def SalesDate(request):
    if request.method == 'POST':
        from_date = request.POST.get('from')
        to_date = request.POST.get('to')

        f_date = from_date.split('-')
        t_date = to_date.split('-')

        start_date = [int(x) for x in f_date]
        end_date = [int(x) for x in t_date]

        orders = Order.objects.filter(is_ordered=True, created_at__gte = datetime.date(start_date[0],start_date[1],start_date[2]),created_at__lte = datetime.date(end_date[0],end_date[1],end_date[2]) )
        
    context = {
        'orders' : orders
    }

    return render(request, 'my_admin/sales_table.html', context )


def SalesMonthly(request, date):
    f =date
    from_date = [2023, f, 1]
    if f==2:
        to_date = [2023, f, 28]
    elif f==4 or f==6 or f==9 or f==11:    
        to_date = [2023, f, 30]
    else:
        to_date = [2023, f, 31]

    orders = Order.objects.filter(is_ordered=True, created_at__gte = datetime.date(from_date[0],from_date[1],from_date[2]),created_at__lte = datetime.date(to_date[0],to_date[1],to_date[2]) )
      
    context = {
        'orders' : orders
    }

    return render(request, 'my_admin/sales_table.html', context)

def SalesYearly(request, date):
    f =date
    from_date = [f, 1, 1]
    to_date = [f, 12, 31]

    orders = Order.objects.filter(is_ordered=True, created_at__gte = datetime.date(from_date[0],from_date[1],from_date[2]),created_at__lte = datetime.date(to_date[0],to_date[1],to_date[2]) )
      
    context = {
        'orders' : orders
    }

    return render(request, 'my_admin/sales_table.html', context)


# Simple CSV Write Operation
def SalesCSV(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['order_id', 'customer', 'order_total', 'payment_mode', 'date'])
    orders = Order.objects.filter(is_ordered=True)
    for order in orders:
        writer.writerow([order.order_number, order.first_name, order.order_total, order.payment.payment_method, order.created_at])
    return response


def SalesXLS(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') # this will make a sheet named Sales Report

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['order_id', 'customer', 'order_total','phone']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body
    font_style = xlwt.XFStyle()
    rows = Order.objects.filter(is_ordered=True).values_list('order_number', 'first_name', 'order_total','phone')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

@login_required(login_url='admin_login')
def CouponTable(request):
    if not request.user.is_superadmin:
        return redirect('home')

    coupons = Coupon.objects.all()
    context = {
        'coupons' : coupons,
    }
    return render(request, 'my_admin/coupon_table.html', context)

@login_required(login_url='admin_login')
def DeleteCoupon(request, id):
    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    return redirect('coupon_table')

@login_required(login_url='admin_login')
def AddCoupon(request):
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        discount = request.POST.get('discount')
        x = Coupon(coupon=coupon,discount=discount)
        x.save()
        return redirect('coupon_table')
    
    return render(request, 'my_admin/add_coupon.html')

@login_required(login_url='admin_login')
def CouponStatus(request, id):
    coupon = Coupon.objects.get(id=id)
    if coupon.is_active:
        coupon.is_active = False
    else:
        coupon.is_active = True
    coupon.save()
    return redirect('coupon_table')




