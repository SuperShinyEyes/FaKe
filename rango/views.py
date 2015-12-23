from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.template.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
# from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.contrib import messages

def is_seller(user):
  return user.groups.filter(name='seller').exists()

def is_buyer(user):
  return user.groups.filter(name='buyer').exists()

def reply_form(request, comment_pk):
  print ">>>> Comment pk:", comment_pk
  return render(request, 'comment_form.html', {"comment_pk":comment_pk})

def test(request):
  a = range(10)
  return render(request, 'test.html', {'a':a, 'product':Product.objects.all()[0], 'user':User.objects.all()[0]})

@login_required
@user_passes_test(is_seller)
def register_new_product(request):
  # A HTTP POST?
  if request.method == 'POST':
    print "This is Post"
    form = ProductForm(request.POST)

    # Have we been provided with a valid form?
    if form.is_valid():
      # Save the new category to the database.
      product = form.save(commit=True)
      print ">>>>>>Validated!!!"
      if 'picture' in request.FILES:
        print ">>>>>>Save picture!!!"
        product.picture = request.FILES['picture']
        product.save()

      # Now call the index() view.
      # The user will be shown the homepage.
      return store(request, 1)
    else:
      # The supplied form contained errors - just print them to the terminal.
      print form.errors
  else:
    # If the request was not a POST, display the form to enter details.
    # http://stackoverflow.com/a/19479357/3067013
    form = ProductForm(initial={'seller':request.user})

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
  return render(request, 'register_new_product.html', {'form': form})


def add_product_to_cart(product, cart):
  if product not in cart.products.all():
    cart.products.add(product)
    '''
    In most situations, an object from DB should be saved after any
    creation/modification. It's cumbersome to figure out every case so I
    prefer to call save() in every case.
    '''
    cart.save()

def get_product_buyers_with_paid_date(product):
  return [(order.user, order.paid_date) for order in product.order_set.all()]

def is_product_in_order(order, product):
  return product in order.products.all()

def already_bought(user, product):
  '''
  True, if the user has already bought the product.
  '''
  orders = user.order_set.all()
  for o in orders:
    if is_product_in_order(o, product):
      return True
  return False

def is_product_seller(user, product):
  return user == product.seller


def post_reply(user, comment_pk, content):
  print "Get comment object pk:", comment_pk
  comment = Comment.objects.get(pk=comment_pk)
  print "Got!!!"
  print comment
  product = comment.product
  reply = Reply(comment=comment, product=product, user=user, content=content)
  reply.save()


@login_required
def product(request, product_id):
  product = get_object_or_404(Product, pk=product_id)
  user = request.user
  redirect_url = '/product/' + str(product_id)
  context = {}
  # context.update(csrf(request))

  if request.POST.get('post_comment', False) == 'True':
    print "Post comment!"
    content = request.POST.get('comment', False)
    product.comment_set.create(user=user, content=content)
    return HttpResponseRedirect(redirect_url)
    # comment = Comment(product=product, user=user, content=content)

  elif request.POST.get('post_reply', False) != False:
    print "Post reply!"
    comment_pk = request.POST.get('post_reply', False)
    content = request.POST.get('content', "No data")
    post_reply(user, comment_pk, content)
    return HttpResponseRedirect(redirect_url)

  elif request.POST.get('delete_reply', False) != False:
    print "Delete reply!"
    reply_pk = request.POST.get('delete_reply', False)
    reply = Reply.objects.get(pk=reply_pk)
    reply.is_active = False
    reply.save()
    print ">>>>>>Redirect: ", redirect_url
    return HttpResponseRedirect(redirect_url)

  elif request.POST.get('delete_comment', False) != False:
    print "Delete comment!"
    comment_pk = request.POST.get('delete_comment', False)
    comment = Comment.objects.get(pk=comment_pk)
    comment.is_active = False
    comment.save()
    sub_replies = comment.reply_set.all()
    for r in sub_replies:
      r.is_active = False
      r.save()
    print ">>>>>>Redirect: ", redirect_url
    return HttpResponseRedirect(redirect_url)

  ## Only buyers can make an order for the product.
  # if request.method == 'POST' and user.user_permissions.filter(codename='can_order').exists():
  elif request.POST.get('add_to_cart', False) == 'True' and is_buyer(user):
    ## get_or_create() returns a length-2 tuple: (object, created)
    ## "created" is a boolean whether it is created or not.
    ## https://docs.djangoproject.com/en/1.8/ref/models/querysets/#get-or-create
    cart = Cart.objects.get_or_create(user=user)[0]
    print 'cart found'
    add_product_to_cart(product, cart)
    return HttpResponseRedirect(reverse('my_cart'))
  elif request.POST.get('delete_product', False) != False:
    product.is_active = False
    product.save()
    return HttpResponseRedirect(redirect_url)

  context['product'] = product
  context['num_comment'] = product.comment_set.filter(is_active=True).count()
  context['comments'] = product.comment_set.filter(is_active=True)

  ## If user has already the product, he cannot make another order
  ## product.html will show "Already bought!" sign
  if already_bought(user, product):
    context['bought'] = True

  elif is_product_seller(user, product):
    print "Yes he is a seller"
    buyers_data = get_product_buyers_with_paid_date(product)
    print buyers_data
    context['buyers_data'] = buyers_data
    context['is_product_seller'] = True

  elif request.method == 'GET':
    product.views += 1
    product.save()

  return render(request, 'product.html', context)

@login_required
def listing_ajax(request):
  product_list = Product.objects.all()
  paginator = Paginator(product_list, 3)

  page = 1
  if request.is_ajax():
    query = request.GET.get('page')
    if query is not None:
      page = query

  try:
    products = paginator.page(page)
  except (EmptyPage, InvalidPage):
    products = paginator.page(paginator.num_pages)
  return render(request, 'list_ajax.html', {'products':products})


def search(product_name, category_name):
  '''
  https://docs.djangoproject.com/en/1.8/ref/models/querysets/#icontains
  '''
  if product_name:
    product_list = Product.objects.filter(name__icontains=product_name)
  else:
    product_list = Product.objects.all()

  if category_name:
    category = get_object_or_404(Category, name=category_name)
    product_list = [p for p in product_list if category in p.categories.all()]

  return product_list

def get_category_value_for_search(request):
  category = request.GET.get('category', False)
  if category == 'all':
    category = False
  return category


def get_page_by_price(price_order_by, context):
  if price_order_by == 'asec':
    context['price_order_by'] = 'desc'
    return Product.objects.order_by('price'), context
  else:
    context['price_order_by'] = 'asec'
    return Product.objects.order_by('-price'), context


def get_store_url(page, base="http://127.0.0.1:8000/store/", price_order_by='', name=''):

  return base + str(page) + '/?price_order_by=' + price_order_by + '/?name=' + name

@login_required
def store_search(request, page=1):
  pass

@login_required
def store(request, page=1):
  ## Using request.GET['query'] will raise error:
  ## MultiValueDictKeyError at /store/1/
  ## Read:
  ## http://stackoverflow.com/a/5895670/3067013
  product_name = request.GET.get('product_name', False)
  category = get_category_value_for_search(request)
  print ">>>>", get_category_value_for_search(request)
  price_order_by = request.GET.get('price_order_by', False)

  ## For multiple <select>
  context = {'categories':Category.objects.all(), 'price_order_by': 'desc'}

  if (product_name or category) and (price_order_by != False):
    pass

  elif price_order_by != False:
    product_list, context = get_page_by_price(price_order_by, context)

  elif product_name or category:
    print "Search is happening!"
    product_list = search(product_name, category)
    context['name_queried'] = True
    print product_name

  else:
    product_list = Product.objects.all()

  paginator = Paginator(product_list, 3)
  context['next_page'] = get_store_url(int(page) - 1, base="http://127.0.0.1:8000/store/", price_order_by=context['price_order_by'], name='')

  try:
    products = paginator.page(page)
  except PageNotAnInteger:
    products = paginator.page(1)
  except EmptyPage:
    products = paginator.page(paginator.num_pages)

  context['products'] = products
  return render(request, 'store.html', context)


@login_required
def my_settings(request):
  user = request.user

  # if request is GET, show the page, else try to change password
  if request.method == 'GET':
    form = PasswordChangeForm(user=user)
    context = {"form": form}
    return render_to_response("my_settings.html", context, context_instance=RequestContext(request))

    # if request is POST, change the password
  elif request.method == 'POST':
    form = PasswordChangeForm(user=user, data=request.POST)
    if form.is_valid():
      # if form is valid, it means old password was correct and new passwords are same
      try:
        # save the new password
        # new_password = form.clean_new_password2()
        # user.set_password(new_password)
        # user.save()
        form.save()
        update_session_auth_hash(request, form.user)
        return HttpResponseRedirect('/')
        # render a message to the user that password is changed
        # context = {
        # "header": "Password changed successfully",
        # "maintext": "Next time login with your new password.",
        # "url": request.build_absolute_uri(reverse('home')),
        # "urltext": "Back to home page"
        # }
        # return render_to_response("message.html", context, context_instance=RequestContext(request))


        # deliver an error message if something went wrong
      except:
        context = {
        "header": "Password change failed",
        "maintext": "Please contact us at mpgamestore@gmail.com.",
        "url": request.build_absolute_uri(reverse('home')),
        "urltext": "Back to home page"
        }
        return render_to_response("message.html", context, context_instance=RequestContext(request))

    else:
      context = {"form": form}
      return render_to_response("my_settings.html", context, context_instance=RequestContext(request))


@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')

def user_login(request):
  # If the request is a HTTP POST, try to pull out the relevant information.
  if request.method == 'POST':
    # Gather the username and password provided by the user.
    # This information is obtained from the login form.
    # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
    # because the request.POST.get('<variable>') returns None, if the value does not exist,
    # while the request.POST['<variable>'] will raise key error exception
    print ">>>> Value:", request.POST
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Use Django's machinery to attempt to see if the username/password
    # combination is valid - a User object is returned if it is.
    user = authenticate(username=username, password=password)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if user:
      # Is the account active? It could have been disabled.
      if user.is_active:
        # If the account is valid and active, we can log the user in.
        # We'll send the user back to the homepage.
        login(request, user)
        return HttpResponseRedirect('/')
      else:
        # An inactive account was used - no logging in!
        return HttpResponse("Your Rango account is disabled.")
    else:
      # Bad login details were provided. So we can't log the user in.
      print "Invalid login details: {0}, {1}".format(username, password)
      return HttpResponse("Invalid login details supplied.")

  # The request is not a HTTP POST, so display the login form.
  # This scenario would most likely be a HTTP GET.
  else:
    # No context variables to pass to the template system, hence the
    # blank dictionary object...
    return render(request, 'login.html', {})

def get_group_name(user_cls):
  groups = {'1':'seller', '2':'buyer'}
  return groups[user_cls]

def add_user_group(user, group):
  '''
  Group is for authorization at views.
  e.g., a buyer is not allowed to access 'My_products' views.
  This function will be called for prepopulating prototyping DB.
  '''
  if user not in group.user_set.all():
    group.user_set.add(user)
    group.save()
  return True

def add_user_permission(user):
  '''
  This is for authentication at HTML level.
  e.g., buyer and seller should have different HTML interfaces.
  http://stackoverflow.com/a/9479717/3067013
  '''
  if user.groups.filter(name='buyer').exists():
    codename = 'can_order'
  else:
    codename = 'can_sell'
  permission = Permission.objects.get(codename=codename)
  user.user_permissions.add(permission)
  user.save()


def update_user_groups_permission(user, member):
  group_name = get_group_name(member.user_cls)
  try:
    group = Group.objects.get_or_create(name=group_name)[0]
  except AttributeError as e:
    print ">>>>> ERROR in update_user_groups"
    print e
    user.delete()
    return False
  else:
    add_user_group(user, group)
    add_user_permission(user)
    return True

def make_order(user, product_ids):
  '''
  example id: u'2015July24-004731-sam'
  '''
  from django.utils import timezone
  now = timezone.now()
  # id = now.strftime("%Y%B%d") + '-' + now.strftime("%H%M%S") + '-' + user.username
  # DataError: value too long for type character varying(20)
  id = len(Order.objects.all())
  order = Order(id=id, user=user)
  order.save()
  print product_ids
  for p_id in product_ids:
    product = Product.objects.get(pk=p_id)
    order.products.add(product)
  order.save()
  return id

def get_total_price(products):
  return sum([p.price for p in products])

def empty_cart(product_ids, cart):
  for id in product_ids:
    product = Product.objects.get(pk=id)
    cart.products.remove(product)

@login_required
@user_passes_test(is_seller)
def my_products(request):
  user = request.user
  products = user.product_set.all()
  context = {'products':products}
  return render(request, 'my_products.html', context)


@login_required
@user_passes_test(is_buyer)
def my_cart(request):
  user = request.user
  cart = Cart.objects.get(user=user)
  if request.method == 'POST':
    product_ids = request.POST.getlist('product_id')
    empty_cart(product_ids, cart)
    id = make_order(user, product_ids)
    print ">>>Order id:", id
    # messages.add_message(request, messages.INFO, id)
    return HttpResponseRedirect('/store/')
    # return HttpResponseRedirect('/my_orders/' + id)

  else:
    products = cart.products.all()
    sum = get_total_price(products)
    context = {'products':products, 'sum':sum}
    return render(request, 'my_cart.html', context)



@login_required
@user_passes_test(is_buyer)
def order_detail(request, order_id):
  order = get_object_or_404(Order, id=order_id)

  if request.method == 'POST':
    order.pay()
    order.save()
    return HttpResponseRedirect('/my_orders')

  total_price = order.get_total_price()
  context = {'products':order.products.all(), 'sum':total_price, 'is_paid':order.is_paid}
  return render(request, 'order_detail.html', context)


@login_required
@user_passes_test(is_buyer)
def my_orders(request):
  user = request.user
  orders = user.order_set.all()
  print ">>>>> DEBUGGING:", user.username, orders
  context = {'orders':orders}
  return render(request, 'my_orders.html', context)

def register(request):

  # A boolean value for telling the template whether the registration was successful.
  # Set to False initially. Code changes value to True when registration succeeds.
  registered=False
  # If it's a HTTP POST, we're interested in processing form data.

  if request.method == 'POST':
    # Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.
    user_form = UserForm(data=request.POST)
    #profile_form = UserProfileForm(data=request.POST)
    userprofile_form = UserProfileForm(data=request.POST)

    # If the two forms are valid...
    if user_form.is_valid() and userprofile_form.is_valid():
      # Save the user's form data to the database.
      user = user_form.save()

      # Now we hash the password with the set_password method.
      # Once hashed, we can update the user object.
      user.set_password(user.password)
      user.save()

      # Now sort out the UserProfile instance.
      # Since we need to set the user attribute ourselves, we set commit=False.
      # This delays saving the model until we're ready to avoid integrity problems.
      profile = userprofile_form.save(commit=False)
      profile.user = user

      # Did the user provide a profile picture?
      # If so, we need to get it from the input form and put it in the UserProfile model.
      if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']

      # Now we save the UserProfile model instance.
      profile.save()

      # Added by Seyoung. Updates user group
      update_user_groups_permission(user, profile)

      # Update our variable to tell the template registration was successful.
      registered = True
      print ">>>>>>Registered!"
      return HttpResponseRedirect('/')
    # Invalid form or forms - mistakes or something else?
    # Print problems to the terminal.
    # They'll also be shown to the user.
    else:
        print user_form.errors, userprofile_form.errors

  # Not a HTTP POST, so we render our form using two ModelForm instances.
  # These forms will be blank, ready for user input.
  else:
    user_form = UserForm()
    userprofile_form = UserProfileForm()

  # Render the template depending on the context.
  context = {'user_form':user_form, 'userprofile_form': userprofile_form, 'registered':registered}
  return render(request, 'join.html', context)

'''
Left it for slug example
def add_page(request, category_name_slug):

  try:
    cat = Category.objects.get(slug=category_name_slug)
  except Category.DoesNotExist:
    cat = None

  if request.method == 'POST':
    form = PageForm(request.POST)
    if form.is_valid():
      if cat:
        page = form.save(commit=False)
        page.category = cat
        page.views = 0
        page.save()
        # probably better to use a redirect here.
        return category(request, category_name_slug)
    else:
      print form.errors
  else:
    form = PageForm()

        # made the change here
  context_dict = {'form':form, 'category': cat, 'category_name_slug': category_name_slug}

  return render(request, 'add_page.html', context_dict)
'''

def add_category(request):
  # A HTTP POST?
  if request.method == 'POST':
    print "This is Post"
    form = CategoryForm(request.POST)

    # Have we been provided with a valid form?
    if form.is_valid():
      # Save the new category to the database.
      form.save(commit=True)

      # Now call the index() view.
      # The user will be shown the homepage.
      return index(request)
    else:
      # The supplied form contained errors - just print them to the terminal.
      print form.errors
  else:
    # If the request was not a POST, display the form to enter details.
    form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
  return render(request, 'add_category.html', {'form': form})
'''
Each view must return a HttpResponse object.
'''

def welcome(reqeust):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Use Django's machinery to attempt to see if the username/password
    # combination is valid - a User object is returned if it is.
    user = authenticate(username=username, password=password)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if user:
      # Is the account active? It could have been disabled.
      if user.is_active:
        # If the account is valid and active, we can log the user in.
        # We'll send the user back to the homepage.
        login(request, user)
        return HttpResponseRedirect('/home')
      else:
        # An inactive account was used - no logging in!
        return HttpResponse("Your Rango account is disabled.")
    else:
      # Bad login details were provided. So we can't log the user in.
      print "Invalid login details: {0}, {1}".format(username, password)
      return HttpResponse("Invalid login details supplied.")

  # The request is not a HTTP POST, so display the login form.
  # This scenario would most likely be a HTTP GET.
  else:
    # No context variables to pass to the template system, hence the
    # blank dictionary object...
    return render(request, 'welcome.html', {})

@login_required
def home(request):
  return render(request, 'home.html', {})


def index(request):
  '''
  The index page is different for logged in users and anonymouse ones.
  '''
  if request.user.is_authenticated():
    return render(request, 'home.html', {})
  else:
    #return HttpResponseRedirect('/login/')
    return render(request, 'login.html', {})


def about(request):

  sentence = "Rango says here is the about page. Go to <a href='/'>home</a>"
  context = {'msg': sentence}
  if request.user in User.objects.all():
    return render(request, 'about_after_login.html', context)
  else:
    return render(request, 'about_before_login.html', context)
  #return HttpResponse(sentence)

def category(request, category_name_slug):
  context = {}
  try:
    category = Category.objects.get(slug=category_name_slug)
    context['category_name'] = category.name
    context['category_slug'] = category_name_slug
    # pages = category.page_set.all()
    # context['pages'] = pages
    context['category'] = category
  except Category.DoesNotExist:
    pass
  return render(request, 'category.html', context)
