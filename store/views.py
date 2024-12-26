from django.shortcuts import render,get_object_or_404
from .models import Category,Product,PhotoGallary,RatingReview
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

#Store page functionality
def store(request,slug=None):
  category=None
  products=None
  if slug != None:
    category=get_object_or_404(Category, slug=slug)
    products=Product.objects.filter(category=category, is_available=True).order_by('id')
    paginator=Paginator(products, 1)
    page=request.GET.get('page')
    paged_product=paginator.get_page(page)
  else:    
    products=Product.objects.all().filter(is_available=True).order_by('id')
    paginator=Paginator(products, 1)
    page=request.GET.get('page')
    paged_product=paginator.get_page(page)
  context={
    'products':paged_product,
    'category':category,
  }
  return render(request,'store/store.html',context)


#product detail functionality
def product_detail(request,category_slug,product_slug):
  try:
    product=Product.objects.get(category__slug=category_slug,slug=product_slug)
  except Exception as e:
    raise e
  reviews =RatingReview.objects.filter(product_id=product.id,status=True)    
  photo_gallary=PhotoGallary.objects.filter(product_id=product.id)  
  context={
    'product':product,
    'photo_gallary':photo_gallary,
    'reviews':reviews,
  }    
  return render(request,'store/product_detail.html',context)   

#product search functionality
def search(request):
  if 'keyword' in request.GET:
    keyword=request.GET['keyword']
    products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(name__icontains=keyword))
    paginator=Paginator(products, 1)
    page=request.GET.get('page')
    paged_product=paginator.get_page(page)
  context={
    'products':paged_product,
  }
  return render(request,'store/store.html',context)

#filter product by maximum and minimum price functionality
def filter(request):
    if request.method == "POST":
        min_price = request.POST.get('minamount')
        max_price = request.POST.get('maxamount')

        # Make sure to validate and handle any possible errors with user input

        products = Product.objects.filter(selling_price__gte=min_price, selling_price__lte=max_price)
        paginator=Paginator(products, 1)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)

        context = {
            'products': paged_product,
        }

        return render(request, 'store/store.html', context)
