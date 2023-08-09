from django.db import models
from django.urls import reverse
from django.db.models import Avg, Count
from account.models import Account

# Create your models here.

#product category model
class Category(models.Model):
  name=models.CharField(max_length=50,unique=True)
  slug=models.SlugField(max_length=50,unique=True)
  description=models.TextField(max_length=255,blank=True)
  image=models.ImageField(upload_to='photo/category',blank=True)

  def product_count(self):
    product_count=Product.objects.filter(category=self).count()
    return product_count

  def get_url(self):
    return reverse('products_by_category',args=[self.slug]) 

  class Meta:
    verbose_name='category'
    verbose_name_plural='categories'

  def __str__(self):
      return self.name

#p
class Product(models.Model):
  name=models.CharField(max_length=200, unique=True)
  slug=models.SlugField(max_length=200, unique=True)
  description=models.TextField(max_length=500, blank=True)
  selling_price=models.IntegerField()
  original_price=models.IntegerField(null=True)
  image=models.ImageField(upload_to='photo/product')
  stock=models.IntegerField()
  is_available=models.BooleanField(default=True)
  category=models.ForeignKey(Category,on_delete=models.CASCADE)
  tag=models.CharField(max_length=100, null=True)
  created_date=models.DateTimeField(auto_now_add=True)
  modified_date=models.DateTimeField(auto_now=True)
  


  def averageReview(self):
    reviews=RatingReview.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
    avg=0
    if reviews['average'] is not None:
      avg =float(reviews['average'])
    return avg 

  def countReview(self):
    reviews=RatingReview.objects.filter(product=self,status=True).aggregate(count=Count('id'))
    count=0
    if reviews['count'] is not None:
      count =int(reviews['count'])
    return count     

  def get_url(self):
    return reverse('product_detail',args=[self.category.slug,self.slug])

  def __str__(self):
    return self.name

class Variation(models.Model):
  product=models.ForeignKey(Product,on_delete=models.CASCADE)  
  size=models.CharField(max_length=100)
  is_active=models.BooleanField(default=True)
  created_date=models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.size   

class RatingReview(models.Model):
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  user=models.ForeignKey(Account,on_delete=models.CASCADE)
  subject=models.CharField(max_length=100,blank=True)
  review=models.TextField(max_length=500,blank=True)
  rating=models.FloatField()
  ip=models.CharField(max_length=20,blank=True)
  status=models.BooleanField(default=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.subject

class PhotoGallary(models.Model):
  product=models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
  image=models.ImageField(upload_to='photo/gallary')

  def __str__(self):
      return self.product.name

  class Meta:
    verbose_name='productgallary'
    verbose_name_plural='product gallery'   