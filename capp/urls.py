from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

urlpatterns=[
path('',views.home,name='home'),
path('login/',views.login,name='login'),
path("logout/", auth_view.LogoutView.as_view(), name="logout"),
path('register/',views.signup,name='register'),
path('ppage',views.productpage,name='ppage'),
path('product/<pid>',views.product,name='product'),
path('admin-index/',views.adminIndex,name='admin-index'),
path('cart/',views.cart,name='cart'),
path('checkout/',views.checkout,name='checkout'),
path('generateOrder/',views.generateOrder,name='generateOrder'),
path("callback/", views.callback, name="callback"),
path("clearCart/", views.clearCart, name="clearCart"),
path("orders/", views.orders, name="orders"),
path("success/", views.success, name="success"),



]