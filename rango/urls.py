from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^test/$', views.test, name='test'),
  url(r'^about/$', views.about, name='about'),
  url(r'^reply_form/(?P<comment_pk>[0-9]+)/$', views.reply_form, name='reply_form'),
  #url(r'^page/(?P<page_id>[0-9]+)/$', views.page_detail, name='page_detail'),
  #url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
  url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
  url(r'^add_category/$', views.add_category, name='add_category'),
  url(r'^register/$', views.register, name='register'),
  url(r'^login/$', views.user_login, name='user_login'),

  url(r'^logout/$', views.user_logout, name='user_logout'),
  url(r'^home/$', views.home, name='home'),
  url(r'^welcome/$', views.welcome, name='welcome'),
  url(r'^my_settings/$', views.my_settings, name='my_settings'),
  url(r'^register_new_product/$', views.register_new_product, name='register_new_product'),

  url(r'^store/(?P<page>[0-9]+)/$', views.store, name='store'),

  url(r'^my_orders/$', views.my_orders, name='my_orders'),
  url(r'^my_orders/(?P<order_id>[\w\-]+)/$', views.order_detail, name='order_detail'),
  url(r'^product/(?P<product_id>[0-9]+)/$', views.product, name='product'),

  url(r'^my_cart/$', views.my_cart, name='my_cart'),
  url(r'^my_products/$', views.my_products, name='my_products'),

  #url(r'^goto/$', views.track_url, name='goto'),
  #url(r'^message/$', views.message, name='message'),
  #url(r'^my_settings/$', views.my_settings, name='my_settings'),
]
