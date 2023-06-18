from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('products/<slug:slug>/',views.store,name='products_by_category'),
    path('product/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('filter/',views.filter,name='filter'),
]
