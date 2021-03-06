from django.conf import settings
from django.conf.urls.static import static

from django.http import request
from django.urls import path, re_path

from products.views import UserProductHistoryView
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', AccountHomeView.as_view(), name='home'),
    path('details/', UserDetailChangeView.as_view(), name='user_update'),
    path('history/product/', UserProductHistoryView.as_view(), name='user_history'),
    re_path(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivateView.as_view(), name='email_activate'),
    re_path(r'^email/resend-activation/$', AccountEmailActivateView.as_view(), name='resend_activation'),
]
