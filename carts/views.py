from django.shortcuts import render, redirect

# Create your views here.
from carts.models import Cart

# 비로그인으로 보고 있다가 로그인을 하게 될 경우, 보고있던 카트를 그대로 그 사람의 아아디로 옮겨주는 로직
from products.models import Product


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    print(product_id)
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show Message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)  # cart_obj.products.add(product_id)
        # return redirect(product_obj.get_absolute_url())
    return redirect("cart:home")
