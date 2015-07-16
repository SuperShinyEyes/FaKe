from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def my_settings(request):
  return render(request, 'rango/my_settings.html', {})

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

def register(request):

  # A boolean value for telling the template whether the registration was successful.
  # Set to False initially. Code changes value to True when registration succeeds.
  registered=False
  # If it's a HTTP POST, we're interested in processing form data.

  if request.method == 'POST':
    # Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    # If the two forms are valid...
    if user_form.is_valid() and profile_form.is_valid():
      # Save the user's form data to the database.
      user = user_form.save()

      # Now we hash the password with the set_password method.
      # Once hashed, we can update the user object.
      user.set_password(user.password)
      user.save()

      # Now sort out the UserProfile instance.
      # Since we need to set the user attribute ourselves, we set commit=False.
      # This delays saving the model until we're ready to avoid integrity problems.
      profile = profile_form.save(commit=False)
      profile.user = user

      # Did the user provide a profile picture?
      # If so, we need to get it from the input form and put it in the UserProfile model.
      if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']

      # Now we save the UserProfile model instance.
      profile.save()

      # Update our variable to tell the template registration was successful.
      registered = True

    # Invalid form or forms - mistakes or something else?
    # Print problems to the terminal.
    # They'll also be shown to the user.
    else:
        print user_form.errors, profile_form.errors

  # Not a HTTP POST, so we render our form using two ModelForm instances.
  # These forms will be blank, ready for user input.
  else:
    user_form = UserForm()
    profile_form = UserProfileForm()

  # Render the template depending on the context.
  context = {'user_form':user_form, 'profile_form': profile_form, 'registered':registered}
  return render(request, 'rango/register.html', context)


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
    return render(request, 'rango/welcome.html', {})

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

def page_detail(request, page_id):
  page = get_object_or_404(Page, pk=page_id)
  context = {'page':page, 'page_id':page_id}
  return render(request, 'rango/page_detail.html', context)

def category(request, category_name_slug):
  context = {}
  try:
    category = Category.objects.get(slug=category_name_slug)
    context['category_name'] = category.name
    context['category_slug'] = category_name_slug
    pages = category.page_set.all()
    context['pages'] = pages
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
