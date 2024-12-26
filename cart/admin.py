from django.contrib import admin
from .models import Wishlist, Cart, CartItem,Coupon,AppliedCoupon
# Register your models here.
admin.site.register(Wishlist)


class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id',)
admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display=('user','product','is_available')
admin.site.register(CartItem,CartItemAdmin)

admin.site.register(Coupon)
admin.site.register(AppliedCoupon)
