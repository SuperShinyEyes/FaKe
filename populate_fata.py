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

def populate():

  u = add_user('sam', 'sam@aol.com', 'seyoung', 'park', 'test')
  add_member(u)
  u = add_user('jenny', 'jenny@aol.com', 'jenny', 'park', 'test')
  add_member(u, '1')
  u = add_user('jon', 'jon@aol.com', 'jon', 'park', 'test')
  add_member(u)
  u = add_user('dan', 'dan@aol.com', 'dan', 'park', 'test')
  add_member(u)
  u = add_user('ken1', 'ken@aol.com', 'ken', 'park', 'test')
  add_member(u)

  for m in Member.objects.all():
    print m

if __name__ == "__main__":
  print ">>>> Starting Fata population script...."
  populate()
