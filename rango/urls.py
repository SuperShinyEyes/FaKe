from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^about/$', views.about, name='about'),
  url(r'^page/(?P<page_id>[0-9]+)/$', views.page_detail, name='page_detail'),
  url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
  url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
  url(r'^add_category/$', views.add_category, name='add_category'),
  url(r'^register/$', views.register, name='register'),
  url(r'^login/$', views.user_login, name='user_login'),
  url(r'^restricted/$', views.restricted, name='restricted'),
  url(r'^logout/$', views.user_logout, name='user_logout'),
  url(r'^home/$', views.home, name='home'),
  url(r'^welcome/$', views.welcome, name='welcome'),
]
