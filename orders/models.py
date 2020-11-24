import math

from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from ecomm.utils import unique_order_id_generator
from products.models import Product

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)


class OrderManagerQueryset(models.query.QuerySet):
    def by_billing_profile(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQueryset(self.model, using=self._db)

    def by_billing_profile(self, request):
        return self.get_queryset().by_billing_profile(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status="created")
        obj = None
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


# Random, Unique
class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, on_delete=models.SET_NULL)
    order_id = models.CharField(max_length=120, blank=True)
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True,
                                         on_delete=models.SET_NULL)
    billing_address = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True,
                                        on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp', '-updated']

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'order_id': self.order_id})

    def get_shipping_status(self):
        if self.status == 'shipped':
            return "Shipped"
        else:
            return "Shipping Soon."

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')

        self.total = formatted_total
        self.save()
        return formatted_total

    def check_done(self):
        shipping_address_required = not self.cart.is_all_digital
        if shipping_address_required and self.shipping_address:
            shipping_done = True
        elif shipping_address_required and not self.shipping_address:
            shipping_done = False
        else:
            shipping_done = True

        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total = self.total
        if billing_profile and billing_address and shipping_done and total > 0:
            return True
        return False

    def update_puchases(self):
        for p in self.cart.products.all():
            obj, created = ProductPurchase.objects.get_or_create(
                order_id=self.order_id,
                product=p,
                billing_profile=self.billing_profile,
            )
        return ProductPurchase.objects.filter(order_id=self.order_id).count()

    def mark_paid(self):
        if self.status != 'paid':
            if self.check_done():
                self.status = 'paid'
                self.save()
                self.update_puchases()
        return self.status

    # generate the order id?


# generate the order total?
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.exists() and qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:  # 처음 생성될 때만 save를 직접 실행하고 그 후로는 pre_save를 통해서 알아서 저장되게 함
        instance.update_total()


post_save.connect(post_save_order, sender=Order)


class ProductPurchaseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)

    def digital(self):
        return self.filter(product__is_digital=True)

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)


class ProductPurchaseManager(models.Manager):
    def get_queryset(self):
        return ProductPurchaseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().filter(refunded=False)

    def digital(self):
        return self.get_queryset().filter(product__is_digital=True)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def products_by_id(self, request):
        qs = self.by_request(request).digital()
        ids_in = [x.product.id for x in qs]
        return ids_in

    def products_by_request(self, request):
        qs = self.products_by_id(request)
        ids_in = [x for x in qs]
        products_qs = Product.objects.filter(id__in=ids_in).distinct()
        return products_qs


class ProductPurchase(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile,
                                        on_delete=models.CASCADE)  # billingprofile.productpurchase_set.all()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # product.productpurchase_set.count()
    refunded = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductPurchaseManager()

    def __str__(self):
        return self.product.title
