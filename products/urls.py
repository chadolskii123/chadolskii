from django.conf import settings
from django.conf.urls.static import static

from django.http import request
from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    # path('featured/', views.ProductFeaturedListView.as_view()),
    # path('featured/<pk>', views.ProductFeaturedDetailView.as_view()),
    # path('fbv/', views.product_list_view),
    # path('<pk>', views.ProductDetailView.as_view()),
    path('<slug>/', views.ProductDetailSlugView.as_view(), name='detail'),
    # path('fbv/<pk>', views.product_detail_view),
]
