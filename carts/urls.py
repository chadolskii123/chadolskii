from django.conf import settings
from django.conf.urls.static import static

from django.http import request
from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_home, name='home'),
    path('checkout/', views.checkout_home, name='checkout'),
    path('update/', views.cart_update, name='update'),

]
