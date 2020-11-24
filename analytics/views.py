from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg, Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from orders.models import Order


class SalesView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/sales.html'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return render(self.request, "400.html", {})
        return super(SalesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args, **kwargs)
        qs = Order.objects.all()
        context['orders'] = qs
        context['recent_orders'] = qs.recent().not_refunded()[:5]
        recent_orders_total = 0
        for i in context['recent_orders']:
            recent_orders_total += i.total
        print(recent_orders_total)
        context['recent_orders_total'] = context['recent_orders'].aggregate(
            Sum("total"),
            Avg("total"),
            # Avg("cart__products__price"),
            # Count("cart__products")
        )
        context['recent_cart_data'] = context['recent_orders'].aggregate(
            # Sum("total"),
            # Avg("total"),
            Avg("cart__products__price"),
            Count("cart__products")
        )
        context['shipped_orders'] = qs.recent().not_refunded().by_status(status='shipped')[:5]
        context['paid_orders'] = qs.recent().not_refunded().by_status(status='paid')[:5]
        return context
