import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import *
from rango.views import *
'''
debugging data for UserProfile()
from store.models import *
c1 = Category('shirt')
c1.update_edt_time()
u1 = User(username='', first_name='seyoung', last_name='park', password='123456')
u1.save()
m1 = UserProfile(user=u1, hp_ddd_no='010', hp_zno='9209', hp_sno='7135', zip_cd='136102', zip_addr='Seoul')
'''

def add_user(username, email, fn, ln, pw ):
  u = User.objects.get_or_create(username=username, email=email, first_name=fn, last_name=ln)[0]
  u.set_password(pw)
  u.save()
  return u

def add_profile(user, user_cls='2'):
  m = UserProfile.objects.get_or_create(user=user, user_cls=user_cls)[0]
  m.save()
  return m

def add_category(name):
  c = Category.objects.get_or_create(name=name)[0]
  c.save()
  return c

def add_product(categories, seller, name, product_num, price, stock, product_info, is_active):
  g = Product.objects.get_or_create(seller=seller, name=name, product_num=product_num, price=price, stock=stock, product_info=product_info, is_active=is_active)[0]
  for c in categories:
    g.categories.add(c)
  g.save()
  return g

def populate():
  ## Register sellers
  u = add_user('jenny', 'jenny@aol.com', 'jenny', 'park', 'test')
  add_profile(u, '1')
  u = add_user('sean', 'sean@aol.com', 'sean', 'park', 'test')
  add_profile(u, '1')
  u = add_user('ted', 'ted@aol.com', 'ted', 'park', 'test')
  add_profile(u, '1')
  u = add_user('sia', 'sia@aol.com', 'sia', 'park', 'test')
  add_profile(u, '1')

  u = add_user('sam', 'sam@aol.com', 'seyoung', 'park', 'test')
  add_profile(u)
  u = add_user('jon', 'jon@aol.com', 'jon', 'park', 'test')
  add_profile(u)
  u = add_user('dan', 'dan@aol.com', 'dan', 'park', 'test')
  add_profile(u)
  u = add_user('ken', 'ken@aol.com', 'ken', 'park', 'test')
  add_profile(u)
  u = add_user('greg', 'greg@aol.com', 'greg', 'park', 'test')
  add_profile(u)
  u = add_user('hal', 'hal@aol.com', 'hal', 'park', 'test')
  add_profile(u)
  u = add_user('yuki', 'yuki@aol.com', 'yuki', 'park', 'test')
  add_profile(u)
  u = add_user('tom', 'tom@aol.com', 'tom', 'park', 'test')
  add_profile(u)
  u = add_user('mac', 'mac@aol.com', 'mac', 'park', 'test')
  add_profile(u)

  categories = ['Men','Women','Europe','Asia','America','Movie','Viral','Music','Education','Cosmetics','Hair','Outdoor','Soccer','Baseball','10s','20s','30s','40s','50s','60s','pop','rock','electronic','psy','wedding']

  for c in categories:
    add_category(c)

  cs = Category.objects.all()

  users = User.objects.all()
  profile = UserProfile.objects.all()
  for profile in profile:
    user = profile.user
    update_user_groups_permission(user, profile)
    print user, profile.user_cls, user.groups.all()

  for u in users:
    add_user_permission(u)

  buyers = [u for u in users if is_buyer(u)]
  sellers = [u for u in users if not is_buyer(u)]
  print sellers
  """
  add_product(cs, sellers[0], name='World', product_num='1234', price=10000, stock=10, product_info="Everything", is_active=True, )
  add_product(cs, sellers[0], name='Seoul', product_num='10', price=400, stock=1, product_info="#Seoul", is_active=True, )
  add_product((cs[0],cs[2],cs[6],cs[7]), sellers[1], name='Viral music which European men likes', product_num='10', price=200, stock=10, product_info="You will see what music men in certain continent likes", is_active=True, )
  add_product([cs[7]], sellers[2], name='Music', product_num='9', price=10, stock=10, product_info="Everything about music", is_active=True, )
  add_product((cs[1],cs[3],cs[5]), sellers[3], name='Asia, Film and women', product_num='3', price=500, stock=10, product_info="Dynamics about Asian Film and women", is_active=True, )
  add_product((cs[4],cs[5]), sellers[0], name='American film', product_num='2', price=300, stock=10, product_info="Everything about American film", is_active=True)
  add_product((cs[1],cs[2]), sellers[2], name='European women', product_num='4', price=120, stock=10, product_info="Everything about European women", is_active=True)
  """
#print Product.objects.all()[0].categories.all()[0].name
  for g in Product.objects.all():
    print g


# for m in UserProfile.objects.all():
#   print m
'''
  for c in Category.objects.all():
    print c
'''

if __name__ == "__main__":
  print ">>>> Starting Fata population script...."
  populate()
