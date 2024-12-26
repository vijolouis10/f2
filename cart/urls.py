from django.urls import path
from . import views

urlpatterns = [
  path('wishlist/',views.wishlist,name='wishlist'),
  path('add-to-wishlist/',views.add_wishlist,name='add-to-wishlist'),
  path('wishlist/count/', views.wishlist_count, name='wishlist_count'),
  path('remove-to-wishlist/',views.remove_wishlist,name="remove-to-wishlist"),

  path('',views.cart,name='cart'),
  path('add-to-cart/',views.add_cart,name='add-to-cart'),
  path('cart/count/', views.cart_count, name='cart_count'),
  path('remove-to-cart/',views.remove_cart,name='remove-to-cart'),
  path('decrease_quantity/',views.decrease_quantity,name='decrease_quantity'),
  path('increase_quantity/',views.increase_quantity,name='increase_quantity'),

  path('checkout/',views.checkout,name='checkout'),

  path('coupon_apply/', views.coupon_apply, name='coupon_apply'),
  path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
]
