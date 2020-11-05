"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import home_page, about_page, contact_page, login_page, register_page

urlpatterns = [
                  path(r'', home_page, name='home'),
                  path(r'about/', about_page),
                  path(r'contact/', contact_page, name='contact'),
                  path(r'login/', login_page, name='login'),
                  path(r'register/', register_page, name='register'),
                  # 부트스트랩 !
                  path(r'bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
                  path(r'products/', include('products.urls'), name='search'),
                  path(r'cart/', include('carts.urls'), name='cart'),
                  path('search/', include('search.urls'), name='search'),
                  path('admin/', admin.site.urls),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
