from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from django.contrib.auth.models import Group, Permission
from django.contrib import messages

def is_seller(user_cls):
  return user_cls == '1'

def add_product_to_cart(product, cart):
  if product not in cart.products.all():
    cart.products.add(product)
    cart.save()


@login_required
def product(request, product_id):
  p = get_object_or_404(Product, pk=product_id)
  user = request.user
  print 'user found'
  if request.method == 'GET':
    p.views += 1
    p.save()
  elif request.method == 'POST' and user.user_permissions.filter(codename='can_order').exists():

    cart = Cart.objects.get_or_create(user=user)[0]
    print 'cart found'
    add_product_to_cart(p, cart)
    return HttpResponseRedirect(reverse('rango:my_cart'))

  context = {'product':p}
  return render(request, 'rango/product.html', context)

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
  return render(request, 'rango/list_ajax.html', {'products':products})

@login_required
def listing(request, page):
  product_list = Product.objects.all()
  paginator = Paginator(product_list, 3)

  try:
    products = paginator.page(page)
  except PageNotAnInteger:
    products = paginator.page(1)
  except EmptyPage:
    products = paginator.page(paginator.num_pages)
  return render(request, 'rango/list.html', {'products':products})

'''
@login_required
def my_settings(request):
  return render(request, 'rango/my_settings.html', {})
'''

@login_required
def edit_user_info(request):
  user = request.user
  context = {'user':user}

  return render(request, 'rango/edit_user_info.html', {})

@login_required
def my_settings(request):
  user = request.user

  # if request is GET, show the page, else try to change password
  if request.method == 'GET':
    form = PasswordChangeForm(user=user)
    context = {"form": form}
    return render_to_response("rango/my_settings.html", context, context_instance=RequestContext(request))

    # if request is POST, change the password
  elif request.method == 'POST':
    form = PasswordChangeForm(user=user, data=request.POST)
    if form.is_valid():
      # if form is valid, it means old password was correct and new passwords are same
      try:
        # save the new password
        new_password = form.clean_new_password2()
        user.set_password(new_password)
        user.save()

        # render a message to the user that password is changed
        context = {
        "header": "Password changed successfully",
        "maintext": "Next time login with your new password.",
        "url": request.build_absolute_uri(reverse('rango:home')),
        "urltext": "Back to home page"
        }
        return render_to_response("rango/message.html", context, context_instance=RequestContext(request))

        # deliver an error message if something went wrong
      except:
        context = {
        "header": "Password change failed",
        "maintext": "Please contact us at mpgamestore@gmail.com.",
        "url": request.build_absolute_uri(reverse('rango:home')),
        "urltext": "Back to home page"
        }
        return render_to_response("rango/message.html", context, context_instance=RequestContext(request))

    else:
      context = {"form": form}
      return render_to_response("rango/my_settings.html", context, context_instance=RequestContext(request))



@login_required
def restricted(request):
  return HttpResponse("Since you're logged in, you can see this!")

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/rango/')

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
        return HttpResponseRedirect('/rango/')
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
    return render(request, 'rango/login.html', {})

def get_group_name(user_cls):
  groups = {'1':'seller', '2':'buyer'}
  return groups[user_cls]

def add_user_group(user, group):
  '''
  This is for authorization at views.
  e.g., a buyer is not allowed to access 'My_products' views.
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

def is_buyer(user):
  return user.groups.filter(name='buyer').exists()

def make_order(user, product_ids):
  '''
  example id: u'2015July24-004731-sam'
  '''
  now = timezone.now()
  id = now.strftime("%Y%B%d") + '-' + now.strftime("%H%M%S") + '-' + user.username
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
@user_passes_test(is_buyer)
def my_cart(request):
  user = request.user
  cart = Cart.objects.get(user=user)
  if request.method == 'POST':
    product_ids = request.POST.getlist('product_id')
    empty_cart(product_ids, cart)
    # print ">>>> key: ", request.POST
    # print ">>>> simple get: ", request.POST.get('product')
    # print ">>>> getlist([]): ", request.POST.getlist('product[]')
    # print ">>>> getlist(): ", request.POST.getlist('product')
    # for p in products:
    #   print p
    id = make_order(user, product_ids)
    print id
    messages.add_message(request, messages.INFO, id)
    return HttpResponseRedirect('/rango/my_orders/' + id)

  else:
    products = cart.products.all()
    sum = get_total_price(products)
    context = {'products':products, 'sum':sum}
    return render(request, 'rango/my_cart.html', context)



@login_required
@user_passes_test(is_buyer)
def order_detail(request, order_id):
  order = get_object_or_404(Order, id=order_id)

  if request.method == 'POST':
    order.pay()
    order.save()
    return HttpResponseRedirect('/rango/my_orders')

  total_price = order.get_total_price()
  context = {'products':order.products.all(), 'sum':total_price, 'is_paid':order.get_is_paid()}
  return render(request, 'rango/order_detail.html', context)


@login_required
@user_passes_test(is_buyer)
def my_orders(request):
  user = request.user
  orders = user.order_set.all()
  print ">>>>> DEBUGGING:", user.username, orders
  context = {'orders':orders}
  return render(request, 'rango/my_orders.html', context)

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
  return render(request, 'rango/join.html', context)

'''
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

  return render(request, 'rango/add_page.html', context_dict)
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
  return render(request, 'rango/add_category.html', {'form': form})
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
        return HttpResponseRedirect('/rango/home')
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
    return render(request, 'rango/welcome.html', {})

@login_required
def home(request):
  return render(request, 'rango/home.html', {})



def index(request):
  '''
  The index page is different for logged in users and anonymouse ones.
  '''
  if request.user.is_authenticated():
    return render(request, 'rango/home.html', {})
  else:
    #return HttpResponseRedirect('/rango/login/')
    return render(request, 'rango/login.html', {})

'''
def index(request):
  popular_categories = Category.objects.order_by('-likes')[:5]
  context = {'categories':popular_categories}

  # Get the number of visits to the site.
  visits = request.session.get('visits')
  if not visits:
    visits = 1
  reset_last_visit_time = False

  last_visit = request.session.get('last_visit')
  # Does the cookie last_visit exist?
  if last_visit:
    # Cast the value to a Python date/time object.
    last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 1:
      visits = visits + 1
      # flat that the cookie last visit needs to be updated
      reset_last_visit_time = True

  else:
    # Cookie last_visit doesn't exist, so flat that it should be set
    reset_last_visit_time = True

  if reset_last_visit_time:
    request.session['last_visit'] = str(datetime.now())
    request.session['visits'] = visits
  context['visits'] = visits

  return render(request, 'rango/index.html', context)
  #return HttpResponse("Rango says hey!<br/><a href='/rango/about'>About</a>")
'''
def about(request):
  sentence = "Rango says here is the about page. Go to <a href='/rango/'>home</a>"
  context = {'msg': sentence}
  return render(request, 'rango/about.html', context)
  #return HttpResponse(sentence)

'''
def page_detail(request, page_id):
  page = get_object_or_404(Page, pk=page_id)
  context = {'page':page, 'page_id':page_id}
  return render(request, 'rango/page_detail.html', context)
'''

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
  return render(request, 'rango/category.html', context)

'''
def category(request, category_id):
  category = get_object_or_404(Category, pk=category_id)
  pages = category.page_set.all()
  context = {'category':category, 'pages':pages}
  return render(request, 'rango/category.html', context)
'''
