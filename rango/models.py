from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import datetime, timedelta

'''
Some methods may seem to repeat the same task.
This is due to the limit of Django Template Language(DTL) in HTML.
DTL cannot call a method with an argument.
It can only run a method without any argument and it should be called
as: some_object.some_method    ===> Without any parenthesis
'''

class OldProfile(models.Model):
    user = models.OneToOneField(User)

    website=models.URLField(blank=True)
    picture=models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username


    # Create your models here.

class UserProfile(models.Model):
  ''' For both buyers and sellers.
      Extends default User class.
      The User() has following Fields:
        username(max_length=30)
        first_name(max_length=30)   - optional
        last_name(max_length=30)    - optional
        email                       - optional
        groups                      - optional
        password:
          - A hash & metadata of the pw. (Django doesn't store the raw pw)
        date_joined
        last_login:
          - returns null if the user has never logged in.

      The User() has following Methods:
        get_username()

      For more, read: https://docs.djangoproject.com/en/1.8/ref/contrib/auth/
      '''
  user = models.OneToOneField(User)

  ## For a restricted set of choices, we use choices parameter.
  SELLER = '1'
  BUYER = '2'
  USER_CHOICES = (
    (SELLER, 'Seller'),
    (BUYER, 'Buyer'),
  )
  user_cls = models.CharField(max_length=1, choices=USER_CHOICES, default=BUYER)
  '''
  hp_ddd_no = models.CharField(max_length=4)
  hp_zno = models.CharField(max_length=4)
  hp_sno = models.CharField(max_length=4)

  tel_ddd_no = models.CharField(max_length=4, null=True, blank=True)
  tel_ano = models.CharField(max_length=4, null=True, blank=True)
  tel_sno = models.CharField(max_length=4, null=True, blank=True)

  zip_cd = models.CharField(max_length=6)
  zip_addr = models.CharField(max_length=150)
  detail_addr = models.CharField(max_length=150, null=True, blank=True)

  ip = models.CharField(max_length=15, null=True, blank=True)
  edit_time = models.CharField(max_length=14, null=True, blank=True)
  '''
  def __str__(self):

    sentence = "id: %s\nname: %s\ndate joined: %s\nlast_login: %s" % (self.user.get_username(), self.user.get_full_name(), self.user.date_joined, self.user.last_login)
    return sentence


class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)
  registeration_time = models.DateTimeField(default=timezone.now, editable=False)
  edited_time = models.DateTimeField(blank=True, null=True)

  def update_edited_time(self):
    self.edited_time = timezone.now()

  def __str__(self):
    sentence = "CATEGORY: %s\nRegistered at: %s" % (self.name, str(self.registeration_time))
    if self.edited_time:
      sentence += "\nLast edit at: %s" % str(self.edited_time)
    return sentence

  class Meta:
    ordering = ('name',)


def get_deadline():
  return datetime.today() + timedelta(days=30)

def get_date(datetime):
  return datetime.strftime('%Y.%B.%d')


def get_filename(full_file_path):
    return full_file_path.split('/')[-1]

def generate_new_filename(instance, full_file_path):
    import uuid, os
    # http://stackoverflow.com/questions/2680391/in-django-changing-the-file-name-of-uploading-file
    filename = get_filename(full_file_path)
    filename = "%s-%s" % (uuid.uuid4(), filename)
    path = "images/"
    return os.path.join(path, filename)


class Product(models.Model):
  categories = models.ManyToManyField(Category)
  seller = models.ForeignKey(User)
  name = models.CharField(max_length=100, blank=False, null=False)
  product_num = models.CharField(max_length=200)

  price = models.DecimalField(max_digits=7,decimal_places=2, blank=False, null=False)
  stock = models.IntegerField(blank=False, null=False)
  sold_amount = models.IntegerField(default=0)
  views = models.IntegerField(default=0)
  expiration_date = models.DateTimeField(null=True)
  #delivery_fee = models.DecimalField(decimal_places=2,blank=False, null=False, max_digits=6)
  #picture = models.ImageField(verbose_name=None, name=None, width_field=None, height_field=None)
  product_info = models.CharField(max_length=4000, blank=False, null=False)
  is_active = models.BooleanField(default=True)
  due_date = models.DateTimeField(default=get_deadline)
  registeration_time = models.DateTimeField(default=timezone.now, editable=False)
  edited_time = models.DateTimeField(blank=True, null=True)
  picture = models.ImageField(upload_to=generate_new_filename, blank=True)
  #cart = models.ForeignKey(Cart, null=True)

  def get_original_stock(self):
    return self.stock + self.sold_amount

  def update_edited_time(self):
    self.edited_time = timezone.now()

  def sold_out_process(self):
    self.is_active = False
    self.expiration_date = timezone.now()

  def sold(self, amount=1):
    if self.stock >= amount:
      self.stock -= amount
      self.sold_amount += amount

      if self.stock == 0:
        self.sold_out_process()

      self.update_edited_time()
    else:
      sentence = "We don't have enough stock!\nStock: %d\nOrder: %d" % (self.stock, amount)
      # raise ValueError(sentence)

  def get_registration_date(self):
    return get_date(self.registeration_time)

  def get_due_date(self):
    return get_date(self.due_date)

  def get_revenue(self):
    pass

  def get_category_names(self):
    names = [c.name for c in self.categories.all()]
    return '/'.join(names)
    # cat_names = []
    # for c in self.categories.all():
    #   cat_names.append(c.name)
    # return '/'.join(cat_names)

  def get_fields(self):
    return [(field.name, field.value_to_string(self)) for field in Product._meta.fields]

  def __unicode__(self):
    cat_names = self.get_category_names()
    sentence = "%s [%s] sold by %s" % (self.name, cat_names, self.seller.username)
    return sentence

  class Meta:
    permissions = (
      ('can_sell', 'Can sell products. Thus he is a seller'),
    )
    ordering = ('-sold_amount', '-registeration_time',)

class Donkey(models.Model):
  pass

class Cart(models.Model):
  user = models.OneToOneField(User)
  products = models.ManyToManyField(Product)

class Order(models.Model):
  '''
  custome id: timezone.now().strftime("%Y%B%d") + username
  '''
  id = models.CharField(max_length=20, primary_key=True)
  user = models.ForeignKey(User)

  products = models.ManyToManyField(Product)
  paid_date = models.DateTimeField(null=True)
  is_delivered = models.BooleanField(default=False)
  is_paid = models.BooleanField(default=False)
  # Run Cron to handle it!!!
  is_closed = models.BooleanField(default=False)

  def get_total_price(self):
    return sum([p.price for p in self.products.all()])

  def get_product_names(self):
    names = [p.name for p in self.products.all()]
    return ', '.join(names)

  def get_paid_date(self):
    return self.paid_date.strftime("%Y.%B.%d.")

  def pay(self):
    self.is_paid = True
    self.is_delivered = True
    self.paid_date = timezone.now()
    for p in self.products.all():
      p.sold()
      p.save()

  def __unicode__(self):
    sentence = "%s --- by --- %s" % (self.id, self.user.username)
    return sentence

  class Meta:
    permissions = (
      ('can_order', 'Can make and view orders'),
    )

class Sales(models.Model):
  user = models.OneToOneField(User)
  products = models.ManyToManyField(Product)

  def get_revenue(self):
    revenue = 0
    for p in products.all():
      revenue += p.price * (p.sold_amount)
    return revenue

class Comment(models.Model):
  '''
  User 'linebreak' for newline characters.
  e.g., {{content|linebreaks}}
  '''
  product = models.ForeignKey(Product)
  user = models.ForeignKey(User)
  content = models.TextField()
  created_time = models.DateTimeField(default=timezone.now, editable=False)
  edited_time = models.DateTimeField(blank=True, null=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.content[:60]

class Reply(models.Model):
  '''
  User 'linebreak' for newline characters.
  e.g., {{content|linebreaks}}
  '''
  comment = models.ForeignKey(Comment)
  product = models.ForeignKey(Product)
  user = models.ForeignKey(User)
  content = models.TextField()
  created_time = models.DateTimeField(default=timezone.now, editable=False)
  edited_time = models.DateTimeField(blank=True, null=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.content[:60]
