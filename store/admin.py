from django.contrib import admin
from .models import Category
from .models import Product,PhotoGallary,RatingReview,Variation
import admin_thumbnails


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields={'slug':('name',)}

admin.site.register(Category,CategoryAdmin)


@admin_thumbnails.thumbnail('image')
class PhotoGallaryInline(admin.TabularInline):
    model = PhotoGallary
    extra = 1

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
  list_display=('name','selling_price','stock','category','modified_date','is_available')
  prepopulated_fields={'slug':('name',)}
  inlines = [PhotoGallaryInline]
admin.site.register(Product,ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
  list_display=('product','size','is_active')
  list_editable=('is_active',)
  list_filter=('product','size')
admin.site.register(Variation,VariationAdmin)

admin.site.register(RatingReview)
