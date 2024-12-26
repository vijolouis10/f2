from . models import Category

def all_category(request):
  categories=Category.objects.all()
  return dict(categories=categories)