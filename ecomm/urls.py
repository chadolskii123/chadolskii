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
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

from accounts.views import guest_register_view, RegisterView, LoginView
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from analytics.views import SalesView, SalesAjaxView
from billing.views import payment_method_view, payment_method_createview
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from orders.views import LibraryView
from .views import home_page, about_page, contact_page, juso_page, introduce_page

urlpatterns = [
                  path(r'', home_page, name='home'),
                  path('juso/', juso_page, name='juso'),
                  path('about/', about_page, name='about'),
                  path('introduce/', introduce_page, name='introduce'),
                  path('contact/', contact_page, name='contact'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('register/guest/', guest_register_view, name='guest_register'),
                  # 부트스트랩 !
                  path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
                  path('library/', LibraryView.as_view(), name='library'),
                  path('products/', include('products.urls'), name='search'),
                  path('cart/', include('carts.urls'), name='cart'),
                  # path(r'accounts/', RedirectView.as_view(url='/account')),
                  path('account/', include('accounts.urls'), name='accounts'),
                  path('accounts/', include('accounts.passwords.urls')),
                  path('orders/', include('orders.urls'), name='orders'),
                  path('api/cart/', cart_detail_api_view, name='api_cart'),
                  path('checkout_address_create_view/', checkout_address_create_view,
                       name='checkout_address_create'),
                  path('checkout_address_reuse_view/', checkout_address_reuse_view,
                       name='checkout_address_reuse'),
                  path('analytics/sales', SalesView.as_view(), name='sales_analytics'),
                  path('analytics/sales/data/', SalesAjaxView.as_view(), name='sales_analytics_data'),
                  path('billing/payment_method/', payment_method_view, name='billing-payment-method'),
                  path('billing/payment_method/create/', payment_method_createview, name='billing-payment-method-api'),
                  path('search/', include('search.urls'), name='search'),
                  path('settings/', RedirectView.as_view(url='/account')),
                  path('settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
                  path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),

                  path('admin/', admin.site.urls),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
