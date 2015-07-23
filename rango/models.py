from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import datetime, timedelta
print timezone.now()

class UserProfile(models.Model):
  user = models.OneToOneField(User)

  website=models.URLField(blank=True)
  picture=models.ImageField(upload_to='profile_images', blank=True)

  def __unicode__(self):
    return self.user.username


    # Create your models here.

class Member(models.Model):
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
  category_name = models.CharField(max_length=100, unique=True)
  registered_time = models.DateTimeField(default=timezone.now, editable=False)
  edited_time = models.DateTimeField(blank=True, null=True)

  def update_edited_time(self):
    self.edited_time = timezone.now()

  def __str__(self):
    sentence = "CATEGORY: %s\nRegistered at: %s" % (self.category_name, str(self.registered_time))
    if self.edited_time:
      sentence += "\nLast edit at: %s" % str(self.edited_time)
    return sentence

  class Meta:
    ordering = ('category_name',)


def get_deadline():
  return datetime.today() + timedelta(days=30)

class Goods(models.Model):
  categories = models.ManyToManyField(Category)
  seller = models.ForeignKey(Member)
  name = models.CharField(max_length=30, blank=False, null=False)
  product_num = models.CharField(max_length=200)

  price = models.DecimalField(max_digits=7,decimal_places=2, blank=False, null=False)
  stock = models.IntegerField(blank=False, null=False)
  sold_amount = models.IntegerField(default=0)
  views = models.IntegerField(default=0)
  expiration_date = models.DateTimeField(null=True)
  #delivery_fee = models.DecimalField(decimal_places=2,blank=False, null=False, max_digits=6)
  #image = models.ImageField(verbose_name=None, name=None, width_field=None, height_field=None)
  product_info = models.CharField(max_length=4000, blank=False, null=False)
  status = models.BooleanField(blank=False, null=False)
  due_date = models.DateTimeField(default=get_deadline)
  registeration_time = models.DateTimeField(default=timezone.now, editable=False)
  edited_time = models.DateTimeField(blank=True, null=True)
  #cart = models.ForeignKey(Cart, null=True)

  def update_edited_time(self):
    self.edited_time = timezone.now()

  def sold_out_process(self):
    self.status = False
    self.expiration_date = timezone.now()

  def sold(self, amount):
    if self.stock >= amount:
      self.stock -= amount
      self.sold_amount += amount

      if self.stock == 0:
        self.sold_out_process()

      self.update_edited_time()
    else:
      sentence = "We don't have enough stock!\nStock: %d\nOrder: %d" % (self.stock, amount)
      raise ValueError(sentence)

  def get_category_names(self):
    cat_names = []
    for c in self.categories.all():
      cat_names.append(c.category_name)
    return '/'.join(cat_names)

  def get_fields(self):
    return [(field.name, field.value_to_string(self)) for field in Goods._meta.fields]

  def __unicode__(self):
    cat_names = self.get_category_names()
    sentence = "%s [%s] sold by %s" % (self.name, cat_names, self.seller.user.first_name)
    return sentence

  class Meta:
    permissions = (
      ('can_sell', 'Can sell products. Thus he is a seller'),
    )
    ordering = ('price',)

class Donkey(models.Model):
  pass

class Cart(models.Model):
  user = models.OneToOneField(User)
  products = models.ManyToManyField(Goods)

class Orders(models.Model):
  pass

class Order(models.Model):
  member = models.ForeignKey(Member, null=True)
  product = models.ForeignKey(Goods, null=True)
  amount = models.IntegerField(default=1)
  orders = models.ForeignKey(Orders, null=True)
  purchased_date = models.DateTimeField(default=timezone.now, null=False)

  def get_total_price(self):
    return product.price * self.amount

  class Meta:
    permissions = (
      ('can_order', 'Can make and view orders'),
    )
