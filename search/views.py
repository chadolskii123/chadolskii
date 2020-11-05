from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from products.models import Product


class SearchProductView(ListView):
    template_name = 'search/view.html'

    def get_context_date(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        # SearchQuery.objects.create(query=query)
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs) :
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)

        if query is not None:
            lookups = Q(title__icontains=query) | Q(description__icontains=query)
            return Product.objects.search(query)
        return Product.objects.featured()
