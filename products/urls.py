from django.conf import settings
from django.conf.urls.static import static

from django.http import request
from django.urls import path, re_path

from .views import *

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    # path('featured/', views.ProductFeaturedListView.as_view()),
    # path('featured/<pk>', views.ProductFeaturedDetailView.as_view()),
    # path('fbv/', views.product_list_view),
    # path('<pk>', views.ProductDetailView.as_view()),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    re_path(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
    # path('fbv/<pk>', views.product_detail_view),
]
