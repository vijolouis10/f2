from django.contrib import admin
from .models import Payment,Order,OrderProduct

# Register your models here.

admin.site.register(Payment)

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    fields=('variations','payment','user','product','quantity','product_price','ordered')

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]
    list_display=('order_number',)

admin.site.register(Order, OrderAdmin)
