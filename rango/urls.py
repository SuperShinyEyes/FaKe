from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^about/$', views.about, name='about'),
  #url(r'^page/(?P<page_id>[0-9]+)/$', views.page_detail, name='page_detail'),
  #url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
  url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
  url(r'^add_category/$', views.add_category, name='add_category'),
  url(r'^register/$', views.register, name='register'),
  url(r'^login/$', views.user_login, name='user_login'),
  url(r'^restricted/$', views.restricted, name='restricted'),
  url(r'^logout/$', views.user_logout, name='user_logout'),
  url(r'^home/$', views.home, name='home'),
  url(r'^welcome/$', views.welcome, name='welcome'),
  url(r'^my_settings/$', views.my_settings, name='my_settings'),
  url(r'^edit_user_info/$', views.edit_user_info, name='edit_user_info'),
  url(r'^listing/(?P<page>[0-9]+)/$', views.listing, name='listing'),

  url(r'^my_orders/$', views.my_orders, name='my_orders'),
  url(r'^my_orders/(?P<order_id>[\w\-]+)/$', views.order_detail, name='order_detail'),
  url(r'^product/(?P<product_id>[0-9]+)/$', views.product, name='product'),
  url(r'^my_cart/$', views.my_cart, name='my_cart'),

  #url(r'^goto/$', views.track_url, name='goto'),
  #url(r'^message/$', views.message, name='message'),
  #url(r'^my_settings/$', views.my_settings, name='my_settings'),
]
