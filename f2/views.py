from django.shortcuts import render
from django.db.models.functions import Random
from store.models import Product
def home(request):
  products = Product.objects.filter(is_available=True).order_by(Random())[:20]
  trending=Product.objects.filter(tag='trending')[:3]
  feature=Product.objects.filter(tag='feature')[:3]
  best=Product.objects.filter(tag='best seller')[:3]
  context={
    'products':products,
    'trending':trending,
    'feature':feature,
    'best':best,
  }
  return render(request,'home.html',context)

  


