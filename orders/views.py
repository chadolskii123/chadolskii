from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from billing.models import BillingProfile
from orders.models import Order, ProductPurchase


class OrderListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Order.objects.by_billing_profile(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'orders/order_detail.html'

    def get_object(self):
        order_id = self.kwargs.get("order_id")
        qs = Order.objects.by_billing_profile(self.request).filter(order_id=self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        return Http404


class LibraryView(LoginRequiredMixin, ListView):
    template_name = 'orders/library.html'

    def get_queryset(self):
        return ProductPurchase.objects.products_by_request(self.request)


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            product_id = data.get('product_id')
            ownership_ids = ProductPurchase.objects.products_by_id(request)
            if int(product_id) in ownership_ids:
                return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404
