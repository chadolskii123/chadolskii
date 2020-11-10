from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from carts.models import Cart
from .models import Product


class ProductListView(ListView):
    template_name = 'products/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.filter(active=True)


class ProductFeaturedListView(ListView):
    template_name = 'products/product_list.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/product_featured_detail.html'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("NOT FOUND!")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmmmmm")
        return instance


class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    # def get_object(self, *args, **kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     instance = Product.objects.get_by_id(pk)
    #     if instance is None:
    #         raise Http404("Product doesn't exist")
    #     return instance
    def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        return Product.objects.filter(pk=pk)


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/product_list.html", context)


def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = get_object_or_404(Product, pk=pk)
    # try :
    #     instance = Product.objects.get(id=4)
    # except Product.DoesNotExist :
    #     print('no product here')
    #     raise Http404("Product doesn't exist")
    # except :
    #     print('huh!?')
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Product doesn't exist")
    #
    # qs = Product.objects.filter(id=pk)
    #
    # if qs.exists() and qs.count() == 1: # len(qs)
    #     instance = qs.first()
    # else :
    #     raise Http404("Product doesn't exist")

    context = {
        'object': instance,
    }
    return render(request, "products/product_detail.html", context)
