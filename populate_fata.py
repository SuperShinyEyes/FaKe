import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import *
'''

debugging data for Member()
from store.models import *
c1 = Category('shirt')
c1.update_edt_time()
u1 = User(username='', first_name='seyoung', last_name='park', password='123456')
u1.save()
m1 = Member(user=u1, hp_ddd_no='010', hp_zno='9209', hp_sno='7135', zip_cd='136102', zip_addr='Seoul')
'''

def add_user(username, email, fn, ln, pw ):
  u = User.objects.get_or_create(username=username, email=email, first_name=fn, last_name=ln)[0]
  u.set_password(pw)
  u.save()
  return u

def add_member(user, user_cls='2'):
  m = Member.objects.get_or_create(user=user, user_cls=user_cls)[0]
  m.save()
  return m

def add_category(name):
  c = Category.objects.get_or_create(category_name=name)[0]
  c.save()
  return c

def add_goods(categories, seller, name, product_num, price, stock, product_info, status):
  g = Goods.objects.get_or_create(seller=seller, name=name, product_num=product_num, price=price, stock=stock, product_info=product_info, status=status)[0]
  for c in categories:
    g.categories.add(c)
  g.save()
  return g

def populate():

  u = add_user('sam', 'sam@aol.com', 'seyoung', 'park', 'test')
  add_member(u)

  u = add_user('jenny', 'jenny@aol.com', 'jenny', 'park', 'test')
  add_member(u, '1')
  u = add_user('sean', 'sean@aol.com', 'sean', 'park', 'test')
  add_member(u, '1')
  u = add_user('ted', 'ted@aol.com', 'ted', 'park', 'test')
  add_member(u, '1')
  u = add_user('sia', 'sia@aol.com', 'sia', 'park', 'test')
  add_member(u, '1')

  u = add_user('jon', 'jon@aol.com', 'jon', 'park', 'test')
  add_member(u)
  u = add_user('dan', 'dan@aol.com', 'dan', 'park', 'test')
  add_member(u)
  u = add_user('ken1', 'ken@aol.com', 'ken', 'park', 'test')
  add_member(u)

  add_category('Men')
  add_category('Women')
  add_category('Europe')
  add_category('Asia')
  add_category('America')
  add_category('Film')
  add_category('Viral')
  add_category('Music')

  cs = Category.objects.all()
  sellers = Member.objects.filter(user_cls='1')
  #print sellers

  add_goods(cs, sellers[0], name='World', product_num='1234', price=10000, stock=10, product_info="Everything", status=True, )
  add_goods((cs[0],cs[2],cs[6],cs[7]), sellers[1], name='Viral music which European men likes', product_num='10', price=200, stock=10, product_info="You will see what music men in certain continent likes", status=True, )
  add_goods([cs[7]], sellers[2], name='Music', product_num='9', price=10, stock=10, product_info="Everything about music", status=True, )
  add_goods((cs[1],cs[3],cs[5]), sellers[3], name='Asia, Film and women', product_num='3', price=500, stock=10, product_info="Dynamics about Asian Film and women", status=True, )
  add_goods((cs[4],cs[5]), sellers[0], name='American film', product_num='2', price=300, stock=10, product_info="Everything about American film", status=True)
  add_goods((cs[1],cs[2]), sellers[2], name='European women', product_num='4', price=120, stock=10, product_info="Everything about European women", status=True)

  #print Goods.objects.all()[0].categories.all()[0].category_name
  for g in Goods.objects.all():
    print g

'''
  for m in Member.objects.all():
    print m

  for c in Category.objects.all():
    print c
'''

if __name__ == "__main__":
  print ">>>> Starting Fata population script...."
  populate()
