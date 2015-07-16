from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
  """docstring for """
  name = models.CharField(max_length=128, unique=True)
  views = models.IntegerField(default=0)
  likes = models.IntegerField(default=0)
  slug = models.SlugField(unique=True)

  def save(self, *args, **kwargs):
    self.slug = slugify(self.name)
    super(Category, self).save(*args, **kwargs)


  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = "Categories"
    ordering = ['name']

class Page(models.Model):
  category = models.ForeignKey(Category)
  title = models.CharField(max_length=128)
  url = models.URLField()
  views = models.IntegerField(default=0)

  def __str__(self):
    return self.title

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
