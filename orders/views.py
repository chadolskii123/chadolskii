from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from billing.models import BillingProfile
from orders.models import Order, ProductPurchase
# from orders.utils import render_to_pdf


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


# Render Template to PDF
# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         data = {
#             'today': datetime.date.today(),
#             'amount': 39.99,
#             'customer_name': 'Cooper Mann',
#             'order_id': 1233434,
#         }
#         pdf = render_to_pdf('pdf/invoice.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')


# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('invoice.html')
#         context = {
#             "invoice_id": 123,
#             "customer_name": "John Cooper",
#             "amount": 1399.99,
#             "today": "Today",
#         }
#         html = template.render(context)
#         pdf = render_to_pdf('invoice.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Invoice_%s.pdf" % ("12341231")
#             content = "inline; filename='%s'" % (filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" % (filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")
