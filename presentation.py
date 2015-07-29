''' models.py '''
class Product(models.Model):
  categories = models.ManyToManyField(Category)
  seller = models.ForeignKey(User)
  name = models.CharField(blank=False, null=False)

''' views.py '''
def is_seller(user):
  return user.groups.filter(name='seller').exists()

@login_required
@user_passes_test(is_seller)
def register_new_product(request):
    pass

''' Use cases '''
product_3 = Product.objects.get(pk=3)
product_3.comment_set.filter(is_active=True).count()
Product.objects.get(name='test').categoreis.all()


def search(product_name, category_name):
  '''product_name: string
     category_name: string
     Get a list of Product objects matching the
     product_name and category_name.'''
  if product_name:
    product_list = Product.objects.filter(name__icontains=product_name)
  else:
    product_list = Product.objects.all()

  if category_name:
    category = get_object_or_404(Category, name=category_name)
    product_list = [p for p in product_list if category in p.categories.all()]

  return product_list


'''
User accesses http://127.0.0.1:8000/rango/store/
'''
## 1. Go to urls.py and match the url pattern
url(r'^store/$', views.store, name='store_main'),
url(r'^store/(?P<page>[0-9]+)/$', views.store, name='store'),
url(r'^register/$', views.register, name='register'),

## 2. Match with the first url pattern. Call its view in views.py
@login_required
def store(request, page=1): pass

## 3. Access DB in the view (views.py)
products = paginator.page(page)
context['products'] = products

## 4. and return an http response object to your web browser
##    and points a template path. (views.py)
return render(request, 'rango/store.html', context)
'''
User finally sees the page
http://127.0.0.1:8000/rango/store/
'''
##
##
##
##
##
##
##
